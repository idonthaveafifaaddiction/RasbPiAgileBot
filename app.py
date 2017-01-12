from tornado import websocket, web, ioloop
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
    ioloop.IOLoop.instance().start()
