'''
Defines a frontend that pipes to a botui JS web interface.

Kipp Freud
31/01/2020
'''

#------------------------------------------------------------------

from util.message import message
from util.server_util import SERVER_APP, SOCKET_SERVER, sendClientMessage, startServer
import util.utilities as ut
from frontend.frontend import CFrontend

#------------------------------------------------------------------

class Cbotuifrontend(CFrontend):
    '''
    A class that interfaces with the botui JS frontend.
    '''
    def __init__(self, **kwargs):
        super(Cbotuifrontend, self).__init__(agent=None)
        self.m_port = 8420
        self._running = False

    def __call__(self, handler):
        self._agent = handler
        return self

    def sendMessage(self, msg):
        '''Send a string msg to the user.'''
        message.logError("This function is depreciated for botui frontend class.",
                         "Cbotuifrontend::sendMessage")
        ut.exit(0)

    def start(self):
        '''Start the message loop.'''
        startServer(SERVER_APP, 8420)

    def stop(self):
        '''Webserver cannot be stopped so this function does nothing.'''
        message.logDebug("The webserver message loop has no stop function. It will end when the program ends.",
                         "Cbotuifrontend::stop")

#------------------------------------------------------------------

#define an instance of this class so it can be used in the server handler functions.
CBotUIFrontend = Cbotuifrontend()

#------------------------------------------------------------------
# 'inline' server functions requiring server class
#------------------------------------------------------------------

@SOCKET_SERVER.on('connect')
async def onConnection(sid, socket):
    message.logDebug("New user '" + sid + "' connected.", "botui_frontend::onConnection")
    #send initial message
    initial_message = CBotUIFrontend.get_initial_message()
    await sendClientMessage(sid, initial_message)

@SOCKET_SERVER.on('disconnect')
def onDisconnection(sid):
    message.logDebug("User '" + sid + "' disconnected.", "botui_frontend::onDisconnection")

@SOCKET_SERVER.on('message')
async def messageReceived(sid, msg):
    if msg == None:
        message.logDebug("Message from user is blank.", "botui_frontend::messageReceived")
        return
    message.logDebug("User '" + sid + "' sent '" + msg + "'.", "botui_frontend::messageReceived")
    #run handler with received msg as input.
    CBotUIFrontend._agent.process_input(msg)
    ret = CBotUIFrontend._agent.get_update()
    if ret:
        for r in ret:
            await sendClientMessage(sid, r)