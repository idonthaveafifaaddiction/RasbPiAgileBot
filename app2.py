import logging
import time
import json

from threading import Timer, Thread
from requests import Session
from signalr import Connection

import breezy_robot_handler

logging.basicConfig(level=logging.DEBUG)

RHANDLER = breezy_robot_handler.RobotHandler()

    
def signal_r_setup():
    with Session() as session:
        # create a connection
        #connection = Connection("https://atbot01.azurewebsites.net/signalr", session)
        connection = Connection("https://dube.azurewebsites.net/signalr", session)
        #connection = Connection("http://localhost:6658/signalr", session)

        # get control hub
        bot = connection.register_hub('BotControl')
        hub = connection.register_hub('WebRtcHub')

        # start a connection
        connection.start()

        t = Timer(.1, RHANDLER.stop)


        hub.server.invoke('registerBot', 'PyBot')
        print('connected to SignalR hub... connection id: ' + connection.token)

        
        # create new control message handler
        def handle_bot_control_request(data):
            print('received: ', data)
            try:
                command = data['Command']
                #RHANDLER.get_sensors()
                if(command == "turn"):
                    RHANDLER.turn(data)
                else:
                    #RHANDLER.go(data)
                    RHANDLER.go_direct(data)
                t.cancel()
                t = Timer(0.50, RHANDLER.stop)
                t.start()
            except:
                pass

        def send_telemetry():
            cnt = 0
            """ Method that runs forever """
            while True:
                cnt = cnt + 1
                # Do something
                j = RHANDLER.get_sensors()
                bot.server.invoke('sendBotTelemetry', j)

                time.sleep(5)

        # receive new chat messages from the hub
        bot.client.on('controllerAt', handle_bot_control_request)

        

        thread = Thread(target=send_telemetry, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()    

        # create error handler
        def print_error(error):
            print('error: ', error)

        # process errors
        connection.error += print_error

        

        # start connection
        #with connection:

            # wait before exit
        connection.wait(None)


if __name__ == '__main__':
    RHANDLER.init_bot()
    signal_r_setup()
