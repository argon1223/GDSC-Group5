from os import path as Path
from getter import Base_Getter

class Downloader(Base_Getter):
    @staticmethod
    def _path(folder, name):
        if name is None:
            name = Path.basename(name)
        return Path.join(folder, name)

    async def download(self, folder, name=None):
        path = self._path(folder, name)

        response = self.get()

        with open(path, "wb") as file:
            async for data in response.content.iter_any():
                file.write(data)
                