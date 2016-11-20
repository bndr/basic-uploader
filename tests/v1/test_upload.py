import io

import aiohttp
from aiohttp.test_utils import unittest_run_loop
from tests import BaseTestCase


class UploadTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_upload_single(self):
        data = io.FileIO(self.test_paths[0])
        request = await self.client.request("POST", "/api/v1/upload", data={'file': data})
        assert request.status == 200
        text = await request.json()
        assert "success" in text


    @unittest_run_loop
    async def test_upload_multiple(self):
        with aiohttp.MultipartWriter('mixed') as mpwriter:
            for index, item in enumerate(self.test_paths):
                part = mpwriter.append(open(item, 'rb'))
                part.set_content_disposition('attachment', filename=self.test_files[index])
            body = b''.join(mpwriter.serialize())
            request = await self.client.request("POST", "/api/v1/upload", data={'file': body}, headers=mpwriter.headers)

            assert request.status == 200
            text = await request.json()
            assert "success" in text