from tornado import websocket, web, ioloop
import json
import logging

logging.basicConfig(level=logging.DEBUG)
c = []


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('BotControl.html')


class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        logging.debug('WebSocket opened')

    def on_message(self, message):
        c = message.split(',')
        logging.debug(message)
        self.write_message(u'You said: X: ' + c[0] + ' Y: ' + c[1])

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

])

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
