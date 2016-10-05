RenderFacade.SetActiveRenderer("victor");
//RenderFacade.SetActiveRenderer("vector2");

var canvas,
    c, // c is the canvas' context 2D
    container,
    halfWidth,
    halfHeight,
    controllerTouchID = -1,
    controllerTouchPos = RenderFacade.RenderFactory(),
    controllerTouchStartPos = RenderFacade.RenderFactory(),
    controllerOutput = RenderFacade.RenderFactory(),
    serverVector = controllerOutput,
        robotPosition = {};


setupCanvas();

var mouseX,
    mouseY,
    // is this running in a touch capable environment?
    touchable = 'createTouch' in document,
    touches = []; // array of touch vectors


setInterval(draw, 1000 / 100);


if (touchable) {
    canvas.addEventListener('touchstart', onTouchStart, false);
    canvas.addEventListener('touchmove', onTouchMove, false);
    canvas.addEventListener('touchend', onTouchEnd, false);

} //else {

canvas.addEventListener('mousedown', onMouseDown, false);
canvas.addEventListener('mousemove', onMouseMove, false);
canvas.addEventListener('mouseup', onMouseUp, false);
//}
window.onorientationchange = resetCanvas;
window.onresize = resetCanvas;

function resetCanvas(e)
{
    // resize the canvas - but remember - this clears the canvas too.
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    halfWidth = canvas.width / 2;
    halfHeight = canvas.height / 2;

    //make sure we scroll to the top left.
    window.scrollTo(0, 0);
}

var frameCount = 0;
function draw()
{
    frameCount++;

    var rate = controllerOutput.magnitude() * 10.0;
    var opacity = .75;// + (Math.sin(frameCount) * .25);
    var baseControllerColor = "rgba(53,133,183,1)";
    var gradientControllerColor = "rgba(53,133,183," + opacity + ")";
    var secondaryControllerColor = "rgba(247,145,29,1";

    c.clearRect(0, 0, canvas.width, canvas.height);

    if (touchable || true) {

        for (var i = 0; i < touches.length; i++) {

            var touch = touches[i];

            if (touch.identifier === controllerTouchID) {

                c.beginPath();
                c.fillStyle = "white";

                c.fillText("vector: " + controllerTouchStartPos.y + ' ' + touch.clientY, 30, 30);

                c.beginPath();
                c.strokeStyle = baseControllerColor;

                c.lineWidth = 6;
                c.arc(controllerTouchStartPos.x, controllerTouchStartPos.y, 10, 0, Math.PI * 2, true);
                c.stroke();
                c.beginPath();
                c.strokeStyle = baseControllerColor;
                c.lineWidth = 2;
                c.arc(controllerTouchStartPos.x, controllerTouchStartPos.y, 40, 0, Math.PI * 2, true);
                c.stroke();


                c.beginPath();
                var grd = c.createRadialGradient(controllerTouchStartPos.x, controllerTouchStartPos.y, 100, controllerTouchStartPos.x, controllerTouchStartPos.y, 260);
                grd.addColorStop(0, "transparent");
                grd.addColorStop(.9, gradientControllerColor);
                grd.addColorStop(1, secondaryControllerColor);

                // Fill with gradient
                c.fillStyle = grd;
                c.strokeStyle = secondaryControllerColor;
                c.lineWidth = 2;
                c.arc(controllerTouchStartPos.x, controllerTouchStartPos.y, 100, 0, Math.PI * 2, true);
                c.stroke();
                c.fill();


                c.beginPath();
                c.strokeStyle = baseControllerColor;
                c.arc(controllerTouchPos.x, controllerTouchPos.y, 40, 0, Math.PI * 2, true);
                c.stroke();

            } else {

                c.beginPath();
                c.fillStyle = "white";
                c.fillText("touch id : " + touch.identifier + " x:" + touch.clientX + " y:" + touch.clientY, touch.clientX + 30, touch.clientY - 30);

                c.beginPath();
                c.strokeStyle = secondaryControllerColor;
                c.lineWidth = "6";
                c.arc(touch.clientX, touch.clientY, 40, 0, Math.PI * 2, true);
                c.stroke();
            }
        }
    } else {

        c.fillStyle = "white";
        c.fillText("mouse : " + mouseX + ", " + mouseY, mouseX, mouseY);

    }

    //draw robot telemetry position
    for (var thisBot in robotPosition) {
        var robotPos = robotPosition[thisBot].pos;
        var botName = robotPosition[thisBot].name;
        var botColor = robotPosition[thisBot].color;


        if (robotPos.x > 0) {
            c.beginPath();
            c.fillStyle = "white";

            c.fillText("Bot Telemetry: name: " + botName + "  pos: " + robotPos.x.toFixed(2) + ' '
                + robotPos.y.toFixed(2), robotPos.x + 50, robotPos.y);

            c.beginPath();
            c.strokeStyle = botColor;

            c.lineWidth = 2;
            c.arc(robotPos.x, robotPos.y, 20, 0, Math.PI * 2, true);
            c.stroke();
            c.beginPath();
            c.strokeStyle = botColor;
            c.lineWidth = 6;
            c.arc(robotPos.x, robotPos.y, 40, 0, Math.PI * 2, true);
            c.stroke();
        }

    }
}

/*
 *	Touch event (e) properties :
 *	e.touches: 			Array of touch objects for every finger currently touching the screen
 *	e.targetTouches: 	Array of touch objects for every finger touching the screen that
 *						originally touched down on the DOM object the transmitted the event.
 *	e.changedTouches	Array of touch objects for touches that are changed for this event.
 *						I'm not sure if this would ever be a list of more than one, but would
 *						be bad to assume.
 *
 *	Touch objects :
 *
 *	identifier: An identifying number, unique to each touch event
 *	target: DOM object that broadcast the event
 *	clientX: X coordinate of touch relative to the viewport (excludes scroll offset)
 *	clientY: Y coordinate of touch relative to the viewport (excludes scroll offset)
 *	screenX: Relative to the screen
 *	screenY: Relative to the screen
 *	pageX: Relative to the full page (includes scrolling)
 *	pageY: Relative to the full page (includes scrolling)
 */

function onTouchStart(e)
{

    for (var i = 0; i < e.changedTouches.length; i++) {
        var touch = e.changedTouches[i];

        if (controllerTouchID < 0) {
            controllerTouchID = touch.identifier;
            controllerTouchStartPos.reset(touch.clientX, touch.clientY);
            controllerTouchPos.copyFrom(controllerTouchStartPos);
            controllerOutput.reset(0, 0);

            window.sendCommand(controllerOutput.x, controllerOutput.y);
            continue;
        }
    }
    touches = e.touches;
}

function onTouchMove(e)
{
    // Prevent the browser from doing its default thing (scroll, zoom)
    e.preventDefault();
    var y;

    for (var i = 0; i < e.changedTouches.length; i++) {
        var touch = e.changedTouches[i];
        if (controllerTouchID === touch.identifier) {


            //  y = (touch.clientY > controllerTouchStartPos.y) ? controllerTouchStartPos.y : touch.clientY;
            y = touch.clientY;

            controllerTouchPos.reset(touch.clientX, y);
            controllerOutput.copyFrom(controllerTouchPos);
            controllerOutput.minusEq(controllerTouchStartPos);
            window.sendCommand(controllerOutput.x, controllerOutput.y);
            break;
        }
    }

    touches = e.touches;

}

function onTouchEnd(e)
{

    touches = e.touches;

    for (var i = 0; i < e.changedTouches.length; i++) {
        var touch = e.changedTouches[i];
        if (controllerTouchID === touch.identifier) {
            controllerTouchID = -1;
            controllerOutput.reset(0, 0);

            window.sendCommand(controllerOutput.x, controllerOutput.y);
            break;
        }
    }

}

function onMouseDown(e) {

    var controlY = ($(window).height() - 150);
    var controlX = ($(window).width() - 150);


    touches[0] = { clientX: controlX, clientY: controlY, identifier: 1 };
    controllerTouchID = 1;
    controllerTouchStartPos.reset(controlX, controlY);
    controllerTouchPos.copyFrom(controllerTouchStartPos);
    controllerOutput.reset(0, 0);

    window.sendCommand(controllerOutput.x, controllerOutput.y);
}

function onMouseMove(e)
{
    e.preventDefault();
    var y;

    if (controllerTouchID === -1) { return; }

    touches[0] = { clientX: e.clientX, clientY: e.clientY, identifier: 1 };

    mouseX = e.clientX;
    mouseY = e.clientY;

    //  y = (touch.clientY > controllerTouchStartPos.y) ? controllerTouchStartPos.y : touch.clientY;
    y = e.clientY;

    controllerTouchPos.reset(e.clientX, y);
    controllerOutput.copyFrom(controllerTouchPos);
    controllerOutput.minusEq(controllerTouchStartPos);
    window.sendCommand(controllerOutput.x, controllerOutput.y);


}
function onMouseUp()
{
    touches.length = 0;
    controllerTouchID = -1;
    controllerOutput.reset(0, 0);

    window.sendCommand(controllerOutput.x, controllerOutput.y);

}

function setupCanvas()
{

    canvas = document.createElement('canvas');
    c = canvas.getContext('2d');
    container = document.createElement('div');
    container.className = "container";

    document.body.appendChild(container);
    container.appendChild(canvas);

    resetCanvas();

    c.strokeStyle = "#ffffff";
    c.lineWidth = 2;
}

  
 
var AppController = function (loadingParams)
{
    this.localVideo_ = $('#local-video')[0];
    this.miniVideo_ = $('#mini-video')[0];
    this.remoteVideo_ = $('#remote-video')[0];
    this.videosDiv_ = $('#videos')[0];

};

AppController.prototype.transitionToActive_ = function ()
{
    reattachMediaStream(this.miniVideo_, this.localVideo_);
    this.activate_(this.remoteVideo_);
    this.activate_(this.miniVideo_);
    this.deactivate_(this.localVideo_);
    this.localVideo_.src = "";
    this.activate_(this.videosDiv_);
    $('.hangup').show();

};
AppController.prototype.transitionToWaiting_ = function ()
{
    this.deactivate_(this.videosDiv_);
    this.localVideo_.src = this.miniVideo_.src;
    this.activate_(this.localVideo_);
    this.deactivate_(this.remoteVideo_);
    this.deactivate_(this.miniVideo_);
    $('.hangup').hide();
};
AppController.prototype.transitionToDone_ = function ()
{
    this.deactivate_(this.localVideo_);
    this.deactivate_(this.remoteVideo_);
    this.deactivate_(this.miniVideo_);
    this.activate_(this.rejoinDiv_);

};
AppController.prototype.activate_ = function (element)
{
    $(element).addClass("active");
};
AppController.prototype.deactivate_ = function (element)
{
    $(element).removeClass("active");
};

$('.hangup').hide();

var ab = new AppController();

function refreshMe()
{

    var list = $('#bot-holder');

    list.empty();

    WebRtcDemo.ViewModel.Bots.forEach(function (item)
   { 

        var txt = item.DisplayName;
        if (item.InSession) {
            txt += ' - (In Session)';
        }
        var li = $('<li/>', { 'data-connectionid': item.ConnectionId })
            .addClass('bot')
            .text(txt)
            .attr('title', 'Click to call')
            .appendTo(list);

    });


}

$('#bot-holder').on('click', '.bot', function ()
{

    // Find the target user's SignalR client id
    var targetConnectionId = WebRtcDemo.ViewModel.Bots[WebRtcDemo.ViewModel.Bots.length - 1].ConnectionId;


    // Initiate a call
    self.hub.server.requestTelepresenceSession(targetConnectionId);

});

// Add handler for the hangup button
$('#controls').on('click', '.hangup', function ()
{
    // Only allow hangup if we are not idle

    self.hub.server.leaveSession();
    WebRtcDemo.ConnectionManager.closeAllConnections();

});

// Kick off the app
//WebRtcDemo.App.start("ShaDu");


$(function ()
{

    var ws = new WebSocket('ws://' + WS_HOST + ':8888/ws');
    var $message = $('#controls');
    var $cordsContainer = $('#cords');



	ws.onopen = function() {
		ws.send("init");
	};
	
	ws.onmessage = function (evt) {
		$message.prepend("<div style='float:left;'>" + evt.data + "</div><br clear='right'/>");
	};


    window.sendCommand = function sendCommand(x, y)
    {
        var cords = ("Thumbstick Input <br />x: " + x + " y: " + y);

        $cordsContainer.html(cords);

        ws.send(x + ',' + y);
    }
});
