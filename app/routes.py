from app.api.v1.download.controller import DownloadView
from app.api.v1.upload.controller import UploadView

from app.frontend.list.controller import ListView
from app.frontend.index.controller import IndexView

routes = [

    # General Frontend Routes
    ('GET', '/', IndexView, 'indexView'),
    ('GET', '/list/', ListView, 'listView'),

    # API Routes
    ('POST', '/api/v1/upload', UploadView, 'uploadView'),
    ('GET', '/api/v1/download/{item}', DownloadView, 'downloadView'),
]