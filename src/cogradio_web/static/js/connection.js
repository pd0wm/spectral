/**
 * Handles everything related to the WebSocket connection.
 */

var Connection = function(){
    var _socket = null;
    var REQUEST_DATA = 0;

    return {
        socket : function(){
            if (_socket === null) {
                _socket = new WebSocket("ws://" + window.location.hostname + ":9000");

                _socket.addEventListener("open", function() {
                    console.log("Connected to " + _socket.url);
                });
                _socket.addEventListener("message", function(event) {
                    setTimeout(function() { Connection.send(REQUEST_DATA); }, 50);
                });
                _socket.addEventListener("close", function() {
                    console.log("Connection closed");
                });
                _socket.addEventListener("error", function() {
                    console.log("An error occurred");
                });
            }

            return _socket;
        },
        close : function(){
            if (_socket !== null) {
                _socket.close(1000);
                _socket = null;
            }
        },
        send : function(data){
            if (_socket === null) {
                console.error("Tried to send message when not connected.");
                return;
            }

            _socket.send(data);
        },
        isOpen : function() {
            return _socket !== null && _socket.readyState == WebSocket.OPEN;
        }
    };
}();
