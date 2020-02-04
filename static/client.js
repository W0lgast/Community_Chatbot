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
        receiveUserTextInput()
    });
});

//send message to user via bot ui
socket.on('show_calendar_message', function(message) {
    botui.message
        .bot({
            type: 'calendar',
            delay: 0,
            content : message
        }).then( function(res) {
            receiveUserCalendarButtonInput()
        });
    });

//send message to user via bot ui
socket.on('show_clickable_message', function(message) {
    botui.message
        .bot({
            type: 'clickable',
            delay: 0,
            content : message
        }).then( function(res) {
            receiveUserConfirmClickableButtonInput()
        });
    });

//show a text box that the user can write in.
var receiveUserTextInput = function () {
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

//show a text box that the user can write in.
var receiveUserCalendarButtonInput = function () {
    botui.action.button({ // let the user perform an action
        delay: 1000,
        action: [
          {
            button_type: "calendar_button",
            text: 'Confirm',
            value: 'Confirm'
          }
        ]
      }).then( function(res) {
        //get the input value
        var message = res.value;
        //send message via socket to server
        socket.emit('message', message)
    });
}

//show a text box that the user can write in.
var receiveUserConfirmClickableButtonInput = function () {
    botui.action.button({ // let the user perform an action
        delay: 1000,
        action: [
          {
            button_type: "confirm_clickable",
            text: 'Confirm',
            value: 'Confirm'
          }
        ]
      }).then( function(res) {
        //get the input value
        var message = res.value;
        //send message via socket to server
        socket.emit('message', message)
    });
}

var main = function () {
    receiveUserTextInput()
}

main()
