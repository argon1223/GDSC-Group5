class Base_Getter():
    get = None

    @classmethod
    def set_get_function(cls, get, **kwargs):
        cls.get = lambda url: get(url, **kwargs)

    def __init__(self, url, /):
        self._url = url

    @property
    def url(self, /):
        return self._url

class HTML_Getter(Base_Getter):
    async def html(self, /):
        response = await self.get(self.url)
        return await response.text()

class Json_Getter(Base_Getter):
    async def json(self, /):
        response = await self.get(self.url)
        return await response.json()

class Soup_Getter(Base_Getter):
    async def soup(self, /):
        html = await self.html()
        return Soup(html, "html.parser")

def set_get_function(get, **kwargs):
    Base_Getter.get = lambda url: get(url, **kwargs)

if __name__ == "__main__":
    import asyncio, aiohttp

    async def main():
        async with aiohttp.ClientSession() as session:
            Json_Getter.get = session.get
            url = "https://www.googleapis.com/youtube/v3/search?key=AIzaSyAkFjDpfEYaOqPCfacULEAHJckcrK2VfDs&channelId=UCHsx4Hqa-1ORjQTh9TYDhww&part=snippet&order=date&maxResults=20&order=date"

            a = Json_Getter(url)

            print(await a.json())
            

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
