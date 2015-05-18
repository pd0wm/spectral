var Connection = function(hostname){
    var _socket = null;
    var openEvent = new Event("socket_open");

    return {
        socket : function(){
            return _socket;
        },
        open : function(){
            if (_socket === null){
                if (!this.hostname) {
                    return null;
                }

                _socket = new WebSocket("ws://" + this.hostname + ":9000");

                _socket.addEventListener("open", function(event) {
                    console.log("Connected to " + _socket.url);
                    document.dispatchEvent(openEvent);
                });
                _socket.addEventListener("close", function(event) {
                    console.log("Connection closed");
                });
                _socket.addEventListener("error", function(event) {
                    console.log("Error: " + event.data);
                });
            }
        },
        close : function(){
            if (_socket !== null) {
                _socket.close(1000);
                _socket = null;
            }
        },
        send : function(data){
            if (_socket === null) {
                return;
            }

            _socket.send(data);
        },
        isOpen : function() {
            return _socket !== null && _socket.readyState == WebSocket.OPEN;
        }
    };
}();
