from rest_framework.serializers import ModelSerializer
from rest_framework import fields
from newzz.crawler import models
import re
class InterestSerializer(ModelSerializer):

    class Meta:
        model = models.Interest
        fields = ('name','slug')

    
class NewsItemSerializer(ModelSerializer):
    site = fields.SerializerMethodField()
    site_url = fields.SerializerMethodField()
    excerpt = fields.SerializerMethodField()
    class Meta:
        model = models.NewsItem
        fields = ('title','excerpt','content','tags','media_url','url','site', 'site_url','created')

    def get_site(self, obj):
        return obj.site.name

    def get_site_url(self, obj):
        return obj.site.link

    def get_excerpt(self,obj):
        return re.sub("<.*?>", "", obj.excerpt).strip()
