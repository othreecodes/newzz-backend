from django.db import models
import uuid
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True

class Site(BaseModel):
    name = models.CharField(max_length=250)
    link = models.URLField()
    rss_feed_url = models.URLField()
    crawl_interval = models.IntegerField(default=10,verbose_name="Crawl Interval in minutes")


    class Meta:
        verbose_name = "Site to Crawl"
        verbose_name_plural = "Sites to Crawl"
        
    def __str__(self):
        return "{}-({})".format(self.name, self.link)

class Interest(BaseModel):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name')
    related = models.ManyToManyField(to='crawler.Interest',related_name='related_interests')
    category = models.ForeignKey('crawler.Interest', blank=True,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class NewsItem(BaseModel):
    site = models.ForeignKey('crawler.Site', on_delete=models.CASCADE)
    title = models.TextField()
    excerpt = models.TextField()
    content = models.TextField()
    tags = ArrayField(models.CharField(max_length=250), blank=True, null=True)
    media_url = models.URLField(blank=True)
    url = models.URLField(unique=True)
    sent = models.BooleanField(default=False)


    def __str__(self):
        return "{} {}".format(self.site, self.title)


class Category(BaseModel):
    name = models.CharField(max_length=250)
