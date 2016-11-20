import datetime
import os
import aiohttp_jinja2
from aiohttp import web
from config import UPLOAD_FOLDER


class ListView(web.View):

    @aiohttp_jinja2.template('list/main.html')
    async def get(self):
        files = self.get_files(UPLOAD_FOLDER)
        return {'files': files}

    def get_files(self, path):
        """
        Goes through the path and get all the filenames and their metadata (size, creation_date)
        :param path: String
        :return: Array[dict]
        """
        files = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if os.path.isfile(full_path):
                files.append({'full_path': path, 'meta': self._get_file_metadata(full_path)})
        return files

    def _get_file_metadata(self, path):
        """
        Get file metadata: Size in MB, date_created as datetime
        :param path: String
        :return: Dict
        """
        stat = os.stat(path)
        date_created = datetime.datetime.fromtimestamp(stat.st_mtime)
        result = {'size': round(stat.st_size / 1024.0 / 1024.0, 4),
                  'filename': os.path.basename(path),
                  'creation_date': date_created}
        return result
