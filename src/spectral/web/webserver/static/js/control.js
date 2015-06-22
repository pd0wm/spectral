/**
 * Handles everything related to control.
 */

 var Control = function() {
    var _socket = null;
    var _elements_by_id = {};
    var _elements_by_key = {};
    websocketInit();

    function processUpdate(data) {
        if (data.settings === true) {
            delete data.settings;
            for (var key in data) {
                if (key in _elements_by_key) {
                    updateElementByKey(key, data[key]);
                }
                else {
                    console.log("Skipping initialisation of setting '" + key + "'");
                }
            }
        }
        else if (data.id) {
            updateElementById(data.id, data.value);
        }
        else if (data.key) {
            updateElementByKey(data.id, data.value);
        }
        else {
            console.error("Could not index element by ID or key");
        }
    };

    function updateElementById(id, value) {
        _elements_by_id[id].update(value);
    }

    function updateElementByKey(key, value) {
        _elements_by_key[key].update(value);
    }

    function websocketInit() {
        if (_socket === null) {
            _socket = new WebSocket("ws://" + window.location.hostname + ":1338");

            _socket.addEventListener("open", function() {
                console.log("Connected to " + _socket.url);
            });
            _socket.addEventListener("message", function(event) {
                var data = JSON.parse(event.data);
                processUpdate(data);
            });
            _socket.addEventListener("close", function() {
                console.log("Connection closed");
            });
            _socket.addEventListener("error", function() {
                console.log("An error occurred");
            });
        }
    };

    function websocketSend(data) {
        if (!Control.running()) {
            console.error("Tried to send message when not connected.");
            return;
        }

        _socket.send(data);
    };

    return {
        register : function (element) {
            _elements_by_id[element.id] = element;
            _elements_by_key[element.key] = element;
        },

        update : function (element, value) {
            if (!Control.running()) {
                window.setTimeout(Control.update, 100, element, value);
                return;
            }

            var message = JSON.stringify({id: element.id, key: element.key, value: value});
            websocketSend(message);
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

