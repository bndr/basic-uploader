import aiohttp_jinja2
from aiohttp import web


class IndexView(web.View):

    @aiohttp_jinja2.template('index/main.html')
    async def get(self):
        return {}
