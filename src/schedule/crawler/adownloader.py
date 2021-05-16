from aiofile import AIOFile, Writer
from downloader import Downloader as old_Downloader

class Downloader(old_Downloader):
    async def download(self, folder, name=None):
        path = self._path(folder, name)

        response = self.get()

        async with AIOFile(filepath, 'wb') as file:
            writer = Writer(file)
            async for data in response.content.iter_any():
                await writer(data)
