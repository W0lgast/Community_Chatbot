'''
Utility functions for launching botui server and sending messages.

Kipp Freud
02/02/2020
'''

#------------------------------------------------------------------

from aiohttp import web
import socketio

from util.message import message
import util.utilities as ut
from frontend.presentation import STANDARD_MSG, CALENDAR_MSG, GENRE_BTN_MSG, EVENT_MSG

#------------------------------------------------------------------

SOCKET_SERVER = socketio.AsyncServer(async_handlers=True,
                                     ping_timeout=200,
                                     reconnection_delay=1)
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
    if not isinstance(msg, tuple):
        message.logError("msg needs to be a tuple of length 2",
                         "server_util::sendClientMessage")
        ut.exit(0)
    if len(msg) != 2:
        message.logError("msg needs to be a tuple of length 2",
                         "server_util::sendClientMessage")
        ut.exit(0)
    message_type = msg[1]
    message_content = msg[0]
    if message_type == STANDARD_MSG:
        await SOCKET_SERVER.emit('show_message', message_content, room=sid)
    elif message_type == CALENDAR_MSG:
        await SOCKET_SERVER.emit('show_message', message_content, room=sid)
        await SOCKET_SERVER.emit('show_calendar_message', "NONE", room=sid)
    elif message_type == GENRE_BTN_MSG:
        msgs = message_content.split(":")
        await SOCKET_SERVER.emit('show_message', msgs[0], room=sid)
        for msg in msgs[1::]:
            await SOCKET_SERVER.emit('show_clickable_message', msg, room=sid)
    elif message_type == EVENT_MSG:
        await SOCKET_SERVER.emit('show_event_message', message_content, room=sid)
    else:
        message.logError("Unknown message type.",
                         "server_util::sendClientMessage")
        ut.exit(0)


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