from newzz.crawler.models import Site
from django.db.models.signals import post_save


def save_new_site(sender, instance, **kwargs):
    #pass

post_save.connect(save_profile, sender=Site)