# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.serializers import serialize
from django.forms.models import model_to_dict

from .models import Site, Interest, NewsItem, Category
from django_celery_beat.models import IntervalSchedule, PeriodicTask
import json

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created',
        'modified',
        'link',
        'rss_feed_url',
        'crawl_interval',
    )
    list_filter = ('created', 'modified')
    search_fields = ('name',)

    def save_model(self, request, obj:Site, form, change):
        obj.save()
        if not change:
            interval = IntervalSchedule()
            interval.every = obj.crawl_interval
            interval.period = IntervalSchedule.MINUTES
            interval.save()

            periodictask = PeriodicTask()
            periodictask.interval = interval
            periodictask.task = "newzz.crawler.tasks.create_new_news_item"
            periodictask.kwargs =  json.dumps(json.loads(serialize('json',[obj,]))[0])
            periodictask.name = obj.id

            periodictask.enabled = True
            periodictask.save()

        else:
            periodictask = PeriodicTask.objects.get(name = obj.pk)
            periodictask.interval.every = obj.crawl_interval
            periodictask.enabled = True
            periodictask.task = "newzz.crawler.tasks.create_new_news_item"
            periodictask.kwargs = json.dumps(json.loads(serialize('json',[obj,]))[0])
            periodictask.interval.save()
            periodictask.save()

        print(change)
        print(obj)


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('slug', 'created', 'modified', 'name','category')
    list_filter = ('created', 'modified', 'category')
    raw_id_fields = ('related',)
    search_fields = ('name', 'slug')
   

@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'site',
        'title',
        'content',
        'tags',
    )
    list_filter = ('created', 'modified', 'site')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified', )
    list_filter = ('created', 'modified')
    search_fields = ('name',)
