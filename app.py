from tornado import websocket, web, ioloop
import json

cl = []

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("BotControl.html")

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)

class ApiHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        self.finish()
        x = self.get_argument("x")
        y = self.get_argument("y")
        data = {"x": x, "y" : y}
        print data
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)

    @web.asynchronous
    def post(self):
        pass

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/api', ApiHandler),
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
