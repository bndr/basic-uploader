from aiohttp.test_utils import unittest_run_loop
from tests import BaseTestCase


class IndexTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_index_page(self):
        request = await self.client.request("GET", "/")
        assert request.status == 200
        text = await request.text()
        assert "File Uploader" in text
        assert "Drag and drop files:" in text