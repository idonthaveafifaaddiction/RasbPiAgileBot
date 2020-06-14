from requests import Session
from signalr import Connection

with Session() as session:
    #create a connection
    #connection = Connection("https://atbot01.azurewebsites.net/signalr", session)
    connection = Connection("http://localhost:6658/signalr", session)

    #get chat hub
    bot = connection.register_hub('BotControl')

    #start a connection
    connection.start()

    #create new chat message handler
    def print_received_message(data):
        print('received: ', data)

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
        connection.wait(60)
