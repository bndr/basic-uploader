import os

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from app.routes import routes
from config import UPLOAD_FOLDER, TEMPLATES_FOLDER


class BaseTestCase(AioHTTPTestCase):
    test_files = ["somebook.pdf", "someotherbook.pdf"]
    test_paths = []
    for item in test_files:
        test_paths.append(os.path.join("./tests/_src/", item))

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
        for item in self.test_files:
            full_path = os.path.join(UPLOAD_FOLDER, item)

            if os.path.isfile(full_path):
                os.remove(full_path)

    def get_app(self, loop):
        """Override the get_app method to return your application.
        """
        # it's important to use the loop passed here.
        app = web.Application(loop=loop, debug=True)

        # Define the views path
        aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATES_FOLDER))

        # route part
        for route in routes:
            app.router.add_route(route[0], route[1], route[2], name=route[3])
        return app