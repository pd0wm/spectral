/**
 * Handles everything related to visualisation.
 */

 var Control = function() {
    var _socket = null;
    websocket_init();

    function update_controls(data) {
        for (var id in data){
            eval(data[id]);
        }
    };

    function websocket_init() {
        if (_socket === null) {
            _socket = new WebSocket("ws://" + window.location.hostname + ":1337");

            _socket.addEventListener("open", function() {
                console.log("Connected to " + _socket.url);
            });
            _socket.addEventListener("message", function(event) {
                var data = JSON.parse(event.data);
                update_controls(data);
            });
            _socket.addEventListener("close", function() {
                console.log("Connection closed");
            });
            _socket.addEventListener("error", function() {
                console.log("An error occurred");
            });
        }
    };

    function websocket_send(data) {
        if (!Control.running()) {
            console.error("Tried to send message when not connected.");
            return;
        }

        _socket.send(data);
    };

    return {
        update : function (id, value) {
            if (!Control.running()) {
                window.setTimeout(Control.update, 100, id, value);
                return;
            }

            var message = JSON.stringify({id: id, value: value});
            websocket_send(message);
        },

        stop : function() {
            if (_socket !== null) {
                _socket.close(1000);
                _socket = null;
            }
        },

        running : function() {
            return _socket !== null && _socket.readyState == WebSocket.OPEN;
        }
    };
}();

