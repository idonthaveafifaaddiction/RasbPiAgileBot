from tornado import websocket, web, ioloop
import json

cl = []

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("BotControl.html")

class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")


app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', EchoWebSocket),
    #(r'/api', ApiHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
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
