import aiohttp


class BaseServiceAPI:
    def __init__(self, base_api, connector=None, headers: dict = None):
        self.BASE_API = base_api
        self.headers = {
            "Content-Type": "application/json",
        }

        if headers is not None:
            self.headers.update(headers)

        self.connector = connector
        self.session = None

    async def init_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(connector=self.connector if self.connector else None)

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def post(self, url, body=None, cookie=None, add_headers=None, params=None, with_base_url=True, data=None):
        await self.init_session()

        full_url = f"{self.BASE_API}{url}" if with_base_url else url
        headers = self.headers.copy()
        print(full_url)
        if add_headers is not None:
            headers.update(add_headers)
        async with self.session.post(full_url, headers=headers, json=body, cookies=cookie, params=params, data=data) as response:
            json = await response.json()
            await self.close()
            return json

    async def get(self, url, params=None, cookie=None, with_base_url=True, add_headers=None):
        await self.init_session()

        api_url = f"{self.BASE_API}{url}" if with_base_url else url
        headers = self.headers.copy()
        if add_headers is not None:
            headers.update(add_headers)
        async with self.session.get(api_url, headers=headers, params=params, cookies=cookie) as response:
            json = await response.json()
            await self.close()
            return json
