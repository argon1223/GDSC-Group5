from dataclasses import dataclass

from django.shortcuts import render
from django.db.models import Q

from subscription.models import Subscription
from .youtube import youtube_crawler

@dataclass
class Video:
    url: str
    thumbnail: str
    channel_name: str
    profile: str
    title: str
    platform: str
    publishTime: str


def schedule_page(request):
    sub_list = Subscription.objects.filter(
        Q(platform='youtube')
    )
    sub_urls = [s.url for s in sub_list]
    #  + ['UC4YaOt1yT-ZeyB0OmxHgolA']

    if len(sub_urls):
        upcomings, videos = youtube_crawler(sub_urls)
        upcomings = upcomings[:4]
        videos = videos[:4]
    else:
        upcomings, videos = [], []

    # print(upcomings, videos)

    upcomings = [
        Video(video['url'], video['thumbnail'], video['channel_name'], video['profile'], video['title'], 'youtube', video['publishTime']) for video in upcomings
    ]
        # Video(
        #     'https://www.youtube.com/watch?v=hyvCXQzQnAM',
        #     'https://i.ytimg.com/vi/hyvCXQzQnAM/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAypHojS4UP2J6y7hj9aTexOd1Xgg',
        #     'https://www.youtube.com/channel/UC4YaOt1yT-ZeyB0OmxHgolA',
        #     'https://yt3.ggpht.com/ytc/AAUvwnhGnnDhdjO7gAkYmd5dvOdKQzgmU6lJfXZfC6CIoA=s88-c-k-c0x00ffffff-no-rj',
        #     '【こんな男大嫌い】束縛する彼氏とサヨナラしたいAIがこちら。',
        #     'youtube',
        #     '2021年5月13日'
        # ),
        # Video(
        #     'https://www.youtube.com/watch?v=ghXopJ9AgFA',
        #     'https://i.ytimg.com/vi/ghXopJ9AgFA/hqdefault_live.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAlYo2BMjcEEyP6IdzrxaEWy5jemg',
        #     'https://www.youtube.com/channel/UCqm3BQLlJfvkTsX_hvm0UmA',
        #     'https://yt3.ggpht.com/ytc/AAUvwnitWcmmZK60TDG8y5aUeQfZlmH9YlBNJ4D1ZSFI=s88-c-k-c0x00ffffff-no-rj',
        #     '【歌枠】第５４回！わためぇ Night Fever!!【角巻わため/ホロライブ４期生】',
        #     'youtube',
        #     '5 小時前'
        # ),
    

    videos = [
        Video(video['url'], video['thumbnail'], video['channel_name'], video['profile'], video['title'], 'youtube', video['publishTime']) for video in videos
    ]

    # print(upcomings, videos)

    context = {
        'upcomings': upcomings,
        'videos': videos,
    }

    return render(request, 'video_page.html', context)
