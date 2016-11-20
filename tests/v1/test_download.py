import io

from aiohttp.test_utils import unittest_run_loop
from tests import BaseTestCase


class DownloadTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_download(self):
        # first upload a file
        data = io.FileIO(self.test_paths[0])
        request = await self.client.request("POST", "/api/v1/upload", data={'file': data})
        assert request.status == 200
        text = await request.json()
        assert "success" in text

        # Then test downloading it
        request = await self.client.request("GET", "/".join(["/api/v1/download", self.test_files[0]]))
        assert request.status == 200
        remote_file = await request.read()
        with open(self.test_paths[0], 'rb') as source:
            real_file_length = len(source.read())
            assert real_file_length > 100
            assert real_file_length == len(remote_file)