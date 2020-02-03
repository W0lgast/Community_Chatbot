//setup the websocket
var socket = io.connect();

//setup the bot ui
var botui = new BotUI('client_bot_ui'),
	address = '';

//send message to user via bot ui
socket.on('show_message', function(message) {
botui.message
    .bot({
        delay: 0,
        content : message
    }).then( function(res) {
        receieveUserInput()
    });
});

//show a text box that the user can write in.
var receieveUserInput = function () {
    botui.action.text({
        delay: 0,
        action: {
            placeholder: ''
        }
    }).then( function(res) {
        //get the input value
        var message = res.value;
        //send message via socket to server
        socket.emit('message', message)
    });
}

var main = function () {
    receieveUserInput()
}

main()
