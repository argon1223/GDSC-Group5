from os import path as Path
import dateutil.parser
from asyncio import create_task
from .crawler.getter import Json_Getter

base_url = "https://www.googleapis.com/youtube/v3"
API_key = "AIzaSyAdboyM3yCJKOfq0lT7GCLY4WcbUenB7u8"

def url_maker(name, **kwargs):
    kwargs.setdefault("key", API_key)
    parameters = "&".join(f"{key}={value}" for key, value in kwargs.items())
    return f"{base_url}/{name}?{parameters}"

class Channel(Json_Getter):
    def __init__(self, channel_id, /):
        self._id = channel_id
        url = url_maker("channels",
            id=channel_id,
            part="snippet"
        )
        super().__init__(url)

    @property
    def id(self, /):
        return self._id

    async def data(self, /):
        json = await self.json()

        return {
            "title": json["items"][0]["snippet"]["title"],
            "thumbnail": json["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        }

class Channel_Searcher(Json_Getter):
    def __init__(self, channel_id, /):
        self._id = channel_id
        url = url_maker("search", 
            channelId=self.id,
            part="snippet",
            type="video",
            order="date",
            maxResults=6,
        )
        super().__init__(url)

    @property
    def id(self, /):
        return self._id

    async def data(self, /):
        json = await self.json()

        upcoming, recents = [], []
        for video_data in json["items"]:
            liveBroadcastContent = video_data["snippet"]["liveBroadcastContent"]
            video_list = recents if liveBroadcastContent == "none" else upcoming

            video_list.append({
                "title": video_data["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={video_data['id']['videoId']}",
                "publishTime": dateutil.parser.parse(video_data["snippet"]["publishTime"]),
                "thumbnail": video_data["snippet"]["thumbnails"]["high"]["url"]
            })

        return upcoming, recents

async def full_data(channel_id):
    tasks1 = create_task(Channel(channel_id).data())
    c = Channel_Searcher(channel_id)
    tasks2 = create_task(c.data())
    channel_data = await tasks1
    upcoming, recents = await tasks2

    for video_list in (upcoming, recents):
        for video_data in video_list:
            video_data["channel_name"] = channel_data["title"]
            video_data["profile"] = channel_data["thumbnail"]
    
    return upcoming, recents

async def crawler_videos(channels_ids):
    import aiohttp
    from asyncio import sleep as asleep

    async with aiohttp.ClientSession() as session:
        Json_Getter.get = session.get

        upcoming, recents = [], []

        for id_ in channels_ids:
            u, c = await create_task(full_data(id_))
            upcoming.extend(u)
            recents.extend(c)
            await asleep(0.2)
        
    return upcoming, recents

def get_id(url):
    return Path.basename(url).split("?")[0]

def youtube_crawler(channels_urls):
    from asyncio import new_event_loop, set_event_loop
    
    channels_ids = [get_id(url) for url in channels_urls]

    loop = new_event_loop()
    set_event_loop(loop)

    upcoming, recents = loop.run_until_complete(crawler_videos(channels_ids))

    upcoming.sort(key=lambda video_data: video_data["publishTime"])
    recents.sort(key=lambda video_data: video_data["publishTime"], reverse=True)

    return upcoming, recents

if __name__ == "__main__":
    from pprint import pprint

    channel1 = "https://www.youtube.com/channel/UC1DCedRgGHBdm81E1llLhOQ"  # peko
    channel2 = "https://www.youtube.com/channel/UCFahBR2wixu0xOex84bXFvg"  # miru
    channel3 = "https://www.youtube.com/channel/UCS9uQI-jC3DE0L4IpXyvr6w"  # coco
    channel4 = "https://www.youtube.com/channel/UCHsx4Hqa-1ORjQTh9TYDhww"  # kiara

    channels = [channel1, channel2, channel3, channel4]

    upcoming, recents = youtube_crawler(channels)

    pprint(upcoming)
    print("="*30)
    pprint(recents)
