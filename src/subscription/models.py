import re

from django.db import models

CATEGORY = {
    'video' : {
        'youtube': r'.*www\.youtube\.com\/channel.*',
        'bahamut': r'.*ani\.gamer\.com\.tw\/animeVideo.*',
    },
    'comic': {
        # TODO: use better reg for exact url for individual page
        'webtoon': r'.*www\.webtoons\.com.*',
    },
}
         

class Subscription(models.Model):
    category = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    url = models.URLField(blank=True)

  
def parse_url(url):
    for category, platform_list in CATEGORY.items():
        for platform, reg in platform_list.items():
            if re.match(reg, url):
                return category, platform

    raise ValueError("Invalid url")


def add_subscription(url):
    try: 
        category, platform = parse_url(url)

        if len(Subscription.objects.filter(
            category=category,
            platform=platform,
            url=url)) == 0:

            Subscription.objects.create(
                category=category,
                platform=platform,
                url=url,
            )

    except ValueError:
        print("error")
        # TODO: add alert for inappropriate input url
        pass


def delete_subscription(pk):
    Subscription.objects.get(id=pk).delete()
