from aiohttp.test_utils import unittest_run_loop
from tests import BaseTestCase


class ListTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_list_view(self):
        request = await self.client.request("GET", "/list/")
        assert request.status == 200
        text = await request.text()
        assert "Files already saved" in text
        assert "Best File Uploader Ever" in text