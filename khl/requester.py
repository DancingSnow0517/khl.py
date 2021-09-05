import asyncio
import logging
from typing import Union

from aiohttp import ClientSession

from .cert import Cert
from .interface import AsyncRunnable

log = logging.getLogger(__name__)

API = f'https://www.kaiheila.cn/api/v3'


class HTTPRequester(AsyncRunnable):
    def __init__(self, cert: Cert):
        self._cert = cert
        self._cs: ClientSession = ClientSession(loop=self.loop)

    def __del__(self):
        asyncio.get_event_loop().run_until_complete(self._cs.close())

    async def request(self, method: str, route: str, **params) -> Union[dict, list]:
        headers = params.pop('headers', {})
        headers['Authorization'] = f'Bot {self._cert.token}'
        params['headers'] = headers

        async with self._cs.request(method, f'{API}/{route}', **params) as res:
            log.debug(f'req: [{route}]({params})')
            rsp = await res.json()
            if rsp['code'] != 0:
                log.error(f'req failed: {rsp}, req:[{route}]({params})')
            else:
                log.debug(f'req done: {rsp}')
            return rsp['data']
