'''
Defines a frontend that pipes to a webpage.

Kipp Freud
28/10/2019
'''

# ------------------------------------------------------------------

from util.message import message
import util.utilities as ut
from frontend.frontend import CFrontend
from flask import Flask, request, Response, render_template

# ------------------------------------------------------------------

CHATBOT_NAME = "KnowBot"
INITIAL_MESSAGE = "How can I help you?"
STOP_HINT = "(enter 'stop' at any time to end session)"
STOP_COMMAND = "stop"
STOP_MESSAGE = "Goodbye, my sweet."
CHANNEL_NAME = "query"

# ------------------------------------------------------------------

# TODO: consider pluggable views instead
# https://flask.palletsprojects.com/en/0.12.x/views/
# CConversation(flask.views.View)

class CWebFrontend(CFrontend):
    '''
    A class for running a terminal frontend.
    '''

    def __init__(self, agent, **kwargs):
        '''
        :param agent: Instance of :class:`CAgent` that handles messages.
        '''
        super(CWebFrontend, self).__init__(agent)
        self.queryHistory = []
        self.responseHistory = []

        # Setup server and routes
        self.server = Flask(__name__)
        self.server.add_url_rule('/', 'home', self.home)
        # TODO: fix this to direct all else to home except query
        #self.server.add_url_rule('/<path:dummy>', 'else_home', self.fallback)
        self.server.add_url_rule('/' + CHANNEL_NAME, \
                                 CHANNEL_NAME, \
                                 self.query, \
                                 methods=['POST'])

    def home(self):
        '''
        page for all queries and responses.
        :return: html with variables filled in
        '''
        return render_template('basic_form.html',
                               bot_name=CHATBOT_NAME,
                               greeting=INITIAL_MESSAGE,
                               hints=STOP_HINT,
                               channel=CHANNEL_NAME
                               )

    def fallback(self, dummy):
        '''
        Catches all other urls and sends to home method
        :param dummy: ignored part of the url
        :return:
        '''
        if dummy == CHANNEL_NAME :
            return self.query(dummy)
        else :
            return self.home()


    def query(self):
        text = request.form['text']

        if not text :
            return

        self.queryHistory.append(text)

        if text.lower() == STOP_COMMAND:
            self.responseHistory.append(STOP_MESSAGE)

        res = self._agent.get_answer(text)
        self.responseHistory.append(res)

        return render_template('basic_form.html',
                               bot_name=CHATBOT_NAME,
                               greeting=INITIAL_MESSAGE,
                               queries=self.queryHistory,
                               answers=self.responseHistory,
                               channel=CHANNEL_NAME
                               )


    def sendMessage(self, msg):
        '''
        Send a string msg to the user.
        '''
        return CHATBOT_NAME + ": " + msg


    def start(self):
        '''
        Start the server.
        '''
        self.server.run()


