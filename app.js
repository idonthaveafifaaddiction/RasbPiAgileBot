var WebRtcDemo = WebRtcDemo || {};

// todo:
//  cleanup: proper module loading
//  cleanup: promises to clear up some of the async chaining
//  feature: multiple chat partners

WebRtcDemo.App = (function (viewModel, connectionManager) {
    var mediaStream;
    

    var self = this;
    self.hub = {};

    function getHub() {
        return self.hub;
    }

    var connect = function(username, onSuccess, onFailure) {
        // Set Up SignalR Signaler
        self.hub = $.connection.webRtcHub;
        var hub = self.hub;

        $.support.cors = true;
        $.connection.hub.url = '/signalr/hubs';

        $.connection.hub.logging = false;

        // Setup client SignalR operations
        setupHubCallbacks(hub);

        $.connection.hub.start()
            .done(function() {
                console.log('connected to SignalR hub... connection id: ' + hub.connection.id);

                if (self.isBot) {
                    hub.server.registerBot(username);
                } else {
                    hub.server.join(username);
                }
               

                if (onSuccess) {
                    onSuccess(hub);
                }
            })
            .fail(function (event) {
                console.log('Failed: ', event);
                if (onFailure) {
                    onFailure(event);
                }
            });
         
    };

    var start = function(name) {
        // Show warning if WebRTC support is not detected
        if (webrtcDetectedBrowser == null) {
            console.log('Your browser doesnt appear to support WebRTC.');
        }

        startSession(name);
    };

    var startAsBot = function (name) {
        self.isBot = true;


        startSession(name);
    };
     

    var startSession = function(username) {
        viewModel.DisplayName = username;

        // Ask the user for permissions to access the webcam and mic
        getUserMedia(
            {
                // Permissions to request
                video: true,
                audio: true
            },
            function(stream) {

                // Now we have everything we need for interaction, so fire up SignalR
                connect(username, function(hub) {

                    // tell the viewmodel our conn id, so we can be treated like the special person we are.
                    viewModel.MyConnectionId = hub.connection.id;

                    // Initialize our client signal manager, giving it a signaler (the SignalR hub) and some callbacks
                    console.log('initializing connection manager');
                    connectionManager.initialize(hub.server, callbacks.onReadyForStream, callbacks.onStreamAdded, callbacks.onStreamRemoved);

                    // Store off the stream reference so we can share it later
                    mediaStream = stream;

                    // Load the stream into a video element so it starts playing in the UI

                    var videoElement = document.querySelector('.video.mine');
                    attachMediaStream(videoElement, mediaStream);

                 
                     
                }, function(event) {
                    console.log('<h4>Failed SignalR Connection</h4> We were not able to connect you to the signaling server.<br/><br/>Error: ' + JSON.stringify(event));
                     
                });
            },
            function(error) { // error callback
                console.log('<h4>Failed to get hardware access!</h4> Do you have another browser type open and using your cam/mic?<br/><br/>You were not connected to the server, because I didn\'t code to make browsers without media access work well. <br/><br/>Actual Error: ' + JSON.stringify(error));
               
            }
        );
    };
 

    var setupHubCallbacks = function(hub) {
        // Hub Callback: Incoming Call
        hub.client.incomingCall = function(callingUser) {
            console.log('incoming call from: ' + JSON.stringify(callingUser));

            if (self.isBot) {
                // auto answer bot
                hub.server.acceptTelepresenceSession(true, callingUser.ConnectionId);
                 
            } 
        };

        // Hub Callback: Call Accepted
        hub.client.callAccepted = function(acceptingUser) {
            console.log('call accepted from: ' + JSON.stringify(acceptingUser) + '.  Initiating WebRTC call and offering my stream up...');

            // Callee accepted our call, let's send them an offer with our video stream
            connectionManager.initiateOffer(acceptingUser.ConnectionId, mediaStream);
             
        };

        // Hub Callback: Call Declined
        hub.client.callDeclined = function(decliningConnectionId, reason) {
            console.log('call declined from: ' + decliningConnectionId);
             
        };

        // Hub Callback: Call Ended
        hub.client.callEnded = function(connectionId, reason) {
            console.log('call with ' + connectionId + ' has ended: ' + reason);
 
            // Close the WebRTC connection
            connectionManager.closeConnection(connectionId);

        };

        hub.client.disconnected = function() {

            connectionManager.closeAllConnections();
        };

        // Hub Callback: Update User List
        hub.client.updateUserList = function (userList) {
           // console.log('Users: ', userList);
            viewModel.Users = userList;
        };

        hub.client.updateBotList = function (botList) {
           // console.log('Bots: ', botList);
            viewModel.Bots = botList;
            if (refreshMe) {
                refreshMe();
            }
        };

        // Hub Callback: WebRTC Signal Received
        hub.client.receiveSignal = function (callingUser, data) {
            console.log(callingUser, data);
            connectionManager.newSignal(callingUser.ConnectionId, data);
        };
    };

    // Connection Manager Callbacks
    var callbacks = {
        onReadyForStream: function(connection) {
            // The connection manager needs our stream
            // todo: not sure I like this
            connection.addStream(mediaStream);
        },
        onStreamAdded: function(connection, event) {
            console.log('binding remote stream to the partner window');

            // Bind the remote stream to the partner window
            var otherVideo = document.querySelector('.video.partner');
            attachMediaStream(otherVideo, event.stream); // from adapter.js
            ab.transitionToActive_();
        },
        onStreamRemoved: function(connection, streamId) {
            // todo: proper stream removal.  right now we are only set up for one-on-one which is why this works.
            console.log('removing remote stream from partner window');

            // Clear out the partner window
            var otherVideo = document.querySelector('.video.partner');
            ab.transitionToWaiting_();
            otherVideo.src = '';

        }
    };

    return {
        start: start, // Starts the UI process
        startAsBot: startAsBot,
        getHub: getHub,
        getStream: function() { // Temp hack for the connection manager to reach back in here for a stream
            return mediaStream;
        }
    };
})(WebRtcDemo.ViewModel, WebRtcDemo.ConnectionManager);
