import logging

from requests import Session
from signalr import Connection
import create
 

logging.basicConfig(level=logging.DEBUG)
robot = create.Create('sim')
  

def signal_r_setup(): 
    with Session() as session:
        #create a connection
        #connection = Connection("http://localhost:6658/signalr", session)
        connection = Connection("https://atbot01.azurewebsites.net/signalr", session)

        #get chat hub
        bot = connection.register_hub('BotControl')
        hub = connection.register_hub('WebRtcHub')

        #start a connection
        connection.start()

        hub.server.invoke('registerBot', 'PyBot')
        print('connected to SignalR hub... connection id: ' + connection.token)
        

        #create new chat message handler
        def print_received_message(data):
            print('received: ', data)
            robot.go(-data['Y'], data['X'])
            bot.server.invoke('sendLocation', data)
            print('sent: ', data)
            

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
            connection.wait(None) # no timeout

if __name__ == '__main__':
    signal_r_setup()
    
