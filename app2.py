import logging

from requests import Session
from signalr import Connection

import breezy_robot_handler

logging.basicConfig(level=logging.DEBUG)

RHANDLER = breezy_robot_handler.RobotHandler()


def signal_r_setup(): 
    with Session() as session:
        #create a connection
        connection = Connection("https://atbot01.azurewebsites.net/signalr", session)
        #connection = Connection("http://localhost:6658/signalr", session)

        #get control hub
        bot = connection.register_hub('BotControl')
        hub = connection.register_hub('WebRtcHub')

        #start a connection
        connection.start()

        hub.server.invoke('registerBot', 'PyBot')
        print('connected to SignalR hub... connection id: ' + connection.token)

        #create new control message handler
        def handle_bot_control_request(data):
            #print('received: ', data)
            try:
                RHANDLER.go(data)
            except:
                pass

        #receive new chat messages from the hub
        bot.client.on('controllerAt', handle_bot_control_request)

        #create error handler
        def print_error(error):
            print('error: ', error)


        #process errors
        connection.error += print_error

        #start connection
        with connection:

            #wait before exit
            connection.wait(None)


if __name__ == '__main__':
    RHANDLER.init_bot()
    signal_r_setup()
    
