import json
import os
import re

from aiohttp import web
from config import UPLOAD_FOLDER


class UploadView(web.View):

    async def post(self):
        reader = await self.request.multipart()
        errors = []
        while True:

            # Fails with exception if a file is a single line over 2 ** 16 in size
            next_file = await reader.next()

            # Some validation here is necessary, otherwise malicious code uploading is possible

            if not next_file:
                break

            filename = next_file.filename
            if not filename:
                break

            full_path = os.path.join(UPLOAD_FOLDER, self._slugify(filename))
            if os.path.isfile(full_path):
                errors.append({filename: "File already exists. Maybe try a different file, or rename the file?"})
                continue
            size = 0

            # If the server crashes at this point, the data will still persist on the filesystem.
            # Maybe some sort of cleanup solution?
            with open(full_path, 'wb') as f:
                while True:
                    chunk = await next_file.read_chunk()  # 8192 bytes by default.
                    if not chunk:
                        break
                    size += len(chunk)
                    f.write(chunk)

        if errors:
            return web.Response(content_type='application/json',
                                text=json.dumps({'errors': errors}),
                                status=400)

        return web.Response(content_type='application/json', text=json.dumps({'success': True}))

    def _slugify(self, value):
        """
        Source: Django Framework
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens.

        :param value: String
        :return: String
        """
        import unicodedata

        # Transform unicode chars like öäü to oau
        value = self._transliterate(value)
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')

        # Strip, lowercase and replace spaces with underscore
        s = value.strip().lower().replace(' ', '_')

        # Remove anything that is not unicode alphanumeric, a dash, or a dot
        # (?u) -> perform the expression as unicode
        # [^-\w.] -> matches dash, alphanumeric, and a dot with negation

        return re.sub(r'(?u)[^-\w.]', '', s)

    def _transliterate(self, value):
        """
        Transliterate russian letters to alphanumeric

        :param value: String
        :return: String
        """
        symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                   u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")

        tr = {ord(a): ord(b) for a, b in zip(*symbols)}
        return value.translate(tr)


