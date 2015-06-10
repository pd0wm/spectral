/**
 * Handles everything related to visualisation.
 */

 var Visualisation = function() {
    var TYPE_NONE = 'none';
    var TYPE_FFT = 'fft';
    var TYPE_SPECTROGRAM = 'spectrogram'

    var DATATYPE_SRC_DATA = 'src_data';
    var DATATYPE_REC_DATA = 'rec_data';
    var DATATYPE_DET_DATA = 'det_data';

    var elements = {};
    var types  = [];
    var _socket = null;

    var title1 =
    {
        "none": 'N/A',
        "fft": 'FFT plot: ',
        "spectrogram": 'Spectrogram: '
    };

    var title2 =
    {
        'src_data': "original data",
        'rec_data': "reconstructed data",
        'det_data': "detection data",
    };

    websocket_init();

    /* Helper functions */

    function title(container, type, datatype) {
        var title = "";
        if (datatype == DATATYPE_DET_DATA) {
            title = "Detector";
        }
        else {
            title = title1[type] + (type == TYPE_NONE ? "" : title2[datatype]);
        }

        container.siblings(".visualisation-header").find("h3").text(title);
    };

    function register(type, datatype) {
        if (type != TYPE_NONE) {
            if (types.indexOf(datatype) == -1) {
                websocket_send(datatype);
            }

            types.push(datatype);
        }
    }

    function update(datatype) {
        var make_request = false;
        for (var element in elements) {
            if (elements[element].data_type == datatype) {
                elements[element].update();
                make_request = true;
            }
        }

        if (make_request) {
            websocket_send(datatype);
        }
    };

    function unregister(container_id) {
        var old_datatype = elements[container_id].data_type;
        types.splice(types.indexOf(old_datatype), 1);

        elements[container_id].destroy();
        delete elements[container_id];
    }

    function update_limits() {
        if (!Visualisation.src_data || !Visualisation.rec_data) {
            return;
        }

        var min = 10 * Math.log10(Math.min(math.min(Visualisation.src_data.data), math.min(Visualisation.rec_data.data)));
        var max = 10 * Math.log10(Math.max(math.max(Visualisation.src_data.data), math.max(Visualisation.rec_data.data)));

        if (min < Visualisation.ymin) {
            Visualisation.ymin = min;
        }

        if (max > Visualisation.ymax) {
            Visualisation.ymax = max;
        }
    }

    /* WebSocket helper functions */

    function websocket_init() {
        if (_socket === null) {
            _socket = new WebSocket("ws://" + window.location.hostname + ":9000");

            _socket.addEventListener("open", function() {
                console.log("Connected to " + _socket.url);
            });
            _socket.addEventListener("message", function(event) {
                var container = JSON.parse(event.data);
                Visualisation[container.dtype] = container;
                update_limits();
                update(container.dtype);
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
        if (!Visualisation.running()) {
            console.error("Tried to send message when not connected.");
            return;
        }

        _socket.send(data);
    };

    /* Public methods and data */

    return {
        src_data: null,
        rec_data: null,
        det_data: null,
        ymin: 0,
        ymax: 0,

        init : function(container_id) {
            if (!Visualisation.running()) {
                window.setTimeout(Visualisation.init, 100, container_id);
                return;
            }

            var type = $('input[name=' + container_id + '-type]:checked', "#" + container_id).val();
            var datatype = $('input[name=' + container_id + '-data]:checked', "#" + container_id).val();
            var container = $("#" + container_id + "-container");
            container.html("");

            if (elements[container_id]) {
                unregister(container_id);
            }

            title(container, type, datatype);

            if (datatype == DATATYPE_DET_DATA) {
                elements[container_id] = new DetPlot(container_id + "-container");
                $("#" + container_id + " .visualisation-type").find('input').prop('disabled', true);
            }
            else if (type == TYPE_NONE) {
                $("#" + container_id + " .visualisation-data").find('input').prop('disabled', true);
            }
            else {
                if (type == TYPE_FFT) {
                    elements[container_id] = new FFTplot(container_id + "-container", datatype);
                }
                else if (type == TYPE_SPECTROGRAM) {
                    elements[container_id] = new SpectroGram(container_id + "-container", datatype);
                }

                $("#" + container_id + " .visualisation-type").find('input').prop('disabled', false);
                $("#" + container_id + " .visualisation-data").find('input').prop('disabled', false);
            }

            register(type, datatype);
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

