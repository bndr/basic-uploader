import os

from aiohttp import web
from config import UPLOAD_FOLDER, CHUNK_SIZE


class DownloadView(web.View):

    async def get(self):

        # item is the filename of the required file
        if 'item' not in self.request.match_info:
            return web.HTTPFound('/')

        file_name = self.request.match_info.get('item')
        full_path = os.path.join(UPLOAD_FOLDER, file_name)

        # check if the file exists
        # Check for directory traversal exploit?
        if not os.path.isfile(full_path):
            return web.Response(text="File Not Found", status=404)

        # Get some stats about the file
        stats = os.stat(full_path)

        # Create a stream response, to push our data in chunks
        # Helps with big files.
        resp = web.StreamResponse(status=200, reason='OK', headers={'Content-Disposition': 'Attachment',
                                                                    'filename': file_name})
        resp.content_length = stats.st_size
        resp.start(self.request)

        with open(full_path, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    return resp
                resp.write(chunk)

        return web.Response(text="File Not Found", status=404)
