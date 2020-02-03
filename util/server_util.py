'''
Utility functions for launching botui server and sending messages.

Kipp Freud
02/02/2020
'''

#------------------------------------------------------------------

from aiohttp import web
import socketio

#------------------------------------------------------------------

SOCKET_SERVER = socketio.AsyncServer(async_handlers=True,
                                     ping_timeout=200)
SERVER_APP = web.Application()
SOCKET_SERVER.attach(SERVER_APP)

#------------------------------------------------------------------

async def index(request):
    with open('./templates/index.html', encoding='utf-8') as f:
        return web.Response(text=f.read(), content_type='text/html')

#------------------------------------------------------------------

SERVER_APP.router.add_get("/", index)
SERVER_APP.router.add_static('/static', 'static')

#------------------------------------------------------------------

async def sendClientMessage(sid, msg):
    """
    Sends a message to specified client using given socket ID.
    """
    await SOCKET_SERVER.emit('show_message', msg, room=sid)

async def sendClientsMessage(msg):
    """
    Sends a message to all connected clients.
    """
    await SOCKET_SERVER.emit('show_message', msg)

#------------------------------------------------------------------

def startServer(server, port=8420):
    """
    Instantiates server on given port.
    """
    web.run_app(server, port=port)