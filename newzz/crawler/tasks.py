from __future__ import absolute_import, unicode_literals

from pprint import pprint

from newzz.taskapp.celery import app
import feedparser
from newzz.crawler import models
from django.db import transaction
from pyfcm import FCMNotification
from .serializers import NewsItemSerializer

push_service = FCMNotification(api_key="AAAAAMmgBJs:APA91bHVrWIXgAH9y7c-ujj3o7b_vS-9Ulo2D6_Z97HUCyocz_3szbHVNTW6zJWplnwiqx-niooVM1lK1A13bR9x-sh9AL17YTDVOc3aNfAwWktSXMQLya4VQdXoRXPYLBbPWcFogrSW")


@app.task()
def task_number_two():
    print("keep alive")


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


@app.task()
def task_send_push_notification_to_client():
    news = models.NewsItem.objects.filter(sent=False)
    interests = models.Interest.objects.all()

    for i in interests:
        items = news.filter(tags__icontains=i.name)
        # items.update({"sent":True})

        news = news.exclude(id__in=items.values_list('id',flat=True))
        data = NewsItemSerializer(items,many=True).data
        for x in chunks(data,1):

            data = {
                "data":x
            }
            pprint(data)
            push_service.notify_topic_subscribers(topic_name=i.slug,data_message=data)


    if len(news) > 0:
        print("more newa", len(news))

        untagged, _ = models.Interest.objects.get_or_create(**{"name": "Uncategorized"})

        # news.update({"tags":})

        data = NewsItemSerializer(untagged, many=True).data
        for x in chunks(data, 1):
            data = {
                "data": x
            }

            push_service.notify_topic_subscribers(topic_name=untagged.slug, data_message=data)

        # data = {
        #     "data": data
        # }
        # push_service.notify_topic_subscribers(topic_name=untagged.slug,data_message=data)

    # push_service.notify_topic_subscribers
    # import pdb; pdb.set_trace()


@app.task()
def create_new_news_item(*args, **kwargs):
    """
    {"model": "crawler.site", "pk": "e3470b65-77d7-401d-9dc4-ed0d7997a908",
     "fields": {"created": "2018-12-07T01:47:57.591Z",
                "modified": "2018-12-07T01:57:52.631Z",
                "name": "Whatsapp",
                "link": "http://whatsapp.com",
                "rss_feed_url": "http://whatsapp.com/rss",
                "crawl_interval": 1}
                }
    :param args:
    :param kwargs:
    :return:
    """
    rss_url = kwargs['fields']['rss_feed_url']
    site = models.Site.objects.get(pk=kwargs['pk'])
    print(kwargs)
    if rss_url:
        data = feedparser.parse(rss_url)

        entries = data.get('entries')

        if entries:
            news_list = []
            for entry in entries:
                with transaction.atomic():
                    item = models.NewsItem()
                    item.site = site
                    item.title = entry['title']
                    item.excerpt = entry.get('summary', '')
                    item.content = ""
                    if entry.get('tags'):
                        item.tags = [x['term'] for x in entry['tags']]

                    if entry.get('media_content'):
                        item.media_url = entry['media_content'][-1]['url']
                    item.url = entry['link']

                    try:
                        item.save()

                        print("added new Item")
                    except Exception as e:
                        # print(e)
                        pass

    print("Creawllwed", kwargs)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10 * 60, task_send_push_notification_to_client.s(), name="send push notification")
