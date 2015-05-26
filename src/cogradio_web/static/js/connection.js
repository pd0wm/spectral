/**
 * Handles everything related to the WebSocket connection.
 */

var Connection = function() {
    var _socket = null;
    var TYPE_SRC_DATA = 'src_data';
    var TYPE_REC_DATA = 'rec_data';
    var TYPE_DET_DATA = 'det_data';
    var srcDataReceived = new Event(TYPE_SRC_DATA);
    var recDataReceived = new Event(TYPE_REC_DATA);
    var detDataReceived = new Event(TYPE_DET_DATA);

    return {
        src_data: null,
        rec_data: null,
        det_data: null,

        socket : function(){
            if (_socket === null) {
                _socket = new WebSocket("ws://" + window.location.hostname + ":9000");

                _socket.addEventListener("open", function() {
                    console.log("Connected to " + _socket.url);
                });
                _socket.addEventListener("message", function(event) {
                    var container = JSON.parse(event.data);
                    switch (container.dtype) {
                        case TYPE_SRC_DATA:
                            Connection.src_data = container;
                            document.dispatchEvent(srcDataReceived);
                            break;
                        case TYPE_REC_DATA:
                            Connection.rec_data = container;
                            document.dispatchEvent(recDataReceived);
                            break;
                        case TYPE_DET_DATA:
                            Connection.det_data = container;
                            document.dispatchEvent(detDataReceived);
                            break;
                    }
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

Connection.socket();
