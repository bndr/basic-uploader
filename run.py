#!/usr/bin/env python

import asyncio

import aiohttp_jinja2
import jinja2
from aiohttp import web

from app.routes import routes
from config import SERVER_URL, SERVER_PORT, TEMPLATES_FOLDER


async def shutdown(server, app, handler):

    server.close()
    await server.wait_closed()
    await app.shutdown()
    await handler.finish_connections(10.0)
    await app.cleanup()

async def create_app(loop):
    app = web.Application(loop=loop, debug=True)

    # Define the views path
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATES_FOLDER))

    # route part
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    return app

async def init(loop):

    app = await create_app(loop)

    # make_handler should be last call, because the state is then frozen
    handler = app.make_handler(debug=True)

    # Run the server on the specified URL and PORT
    server = loop.create_server(handler, '0.0.0.0', SERVER_PORT)
    return server, handler, app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    serv_generator, handler, app = loop.run_until_complete(init(loop))
    server = loop.run_until_complete(serv_generator)
    print('serving on', server.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Stopping')
    finally:
        loop.run_until_complete(shutdown(server, app, handler))
        loop.close()
    print('Finished')