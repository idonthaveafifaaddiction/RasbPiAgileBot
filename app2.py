from tornado import websocket, web, ioloop
from requests import Session
from signalr import Connection

import json
import logging

import breezy_robot_handler

logging.basicConfig(level=logging.DEBUG)
c = []
rhandle = breezy_robot_handler.RobotHandler()


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('BotControl.html')


class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        logging.debug('WebSocket opened')

    def on_message(self, message):
        if message == 'init':
            return
        c = message.split(',')
        x = int(float(c[1])) * -1 # Negate linear velocity
        y = int(float(c[0]))
        #logging.debug(message)
        self.write_message(u'linear V: ' + str(x) + ' angular V: ' + str(y))
        try:
            rhandle.go(x, y)
        except:
            pass

    def on_close(self):
        logging.debug('WebSocket closed')


def signalRSetup(): 
    with Session() as session:
        #create a connection
        connection = Connection("https://atbot01.azurewebsites.net/signalr", session)

        #get chat hub
        bot = connection.register_hub('BotControl')

        #start a connection
        connection.start()

        #create new chat message handler
        def print_received_message(data):
            print('received: ', data)
            #j = json.loads(data)
            #print j['X']
            #print j['Y']
            try:
                rhandle.go(data['X'], data['Y'])
            except:
                pass

        #receive new chat messages from the hub
        bot.client.on('controllerAt', print_received_message)

        #create error handler
        def print_error(error):
            print('error: ', error)


        #process errors
        connection.error += print_error

        #connection.start()

        #start connection, optionally can be connection.start()
        with connection:

            #post new message
            #bot.server.invoke('sendLocation', 'RaspPi')

            #wait a second before exit
            connection.wait(300)


app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', EchoWebSocket),
    #(r'/api', ApiHandler),
    (r'/(config.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(BotControl.css)', web.StaticFileHandler, {'path': './'}),
    (r'/(adapter.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(jquery-1.10.2.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(jquery.signalR-2.2.0.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(Vector2.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(victor.min.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(VectorFacade.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(connectionManager.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(viewModel.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(app.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(BotControl.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(rx.all.min.js)', web.StaticFileHandler, {'path': './'}),
    (r'/(rx.all.map)', web.StaticFileHandler, {'path': './'})
])

if __name__ == '__main__':
    rhandle.init_bot('trash')
    app.listen(8888)
    signalRSetup()
    ioloop.IOLoop.instance().start()
    
