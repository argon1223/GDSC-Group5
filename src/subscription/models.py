import re

from django.db import models

from schedule.youtube import youtube_crawler

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
    channel_name = models.CharField(max_length=100)
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
        print(category, platform, [url.split('/')[-1]])

        # url == https://www.youtube.com/channel/UCbJM_Y06iuUOl3hVPqYcvng
        name = youtube_crawler([url.split('/')[-1]])[1][0]['channel_name']

        if len(Subscription.objects.filter(url=url)) == 0:

            Subscription.objects.create(
                category=category,
                platform=platform,
                url=url,
                channel_name=name,
            )
    except KeyError:
        print('The request cannot be completed because you have exceeded api quota.')

    except ValueError as e:
        print(e)
        # TODO: add alert for inappropriate input url


def delete_subscription(pk):
    Subscription.objects.filter(id=pk).delete()
