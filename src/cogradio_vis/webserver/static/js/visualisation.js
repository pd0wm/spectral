/**
 * Handles everything related to visualisation.
 */

 var Visualisation = function() {
    var TYPE_NONE = 'none';
    var TYPE_FFT = 'fft';
    var TYPE_SPECTROGRAM = 'spectrogram';
    var TYPE_SWEEP = 'sweep';

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
        "spectrogram": 'Spectrogram: ',
        "sweep": 'Sweep - '
    };

    var title2 =
    {
        'src_data': "original data",
        'rec_data': "reconstructed data",
        'det_data': "detection data",
    };

    websocketInit();

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
                websocketSend(datatype);
            }

            types.push(datatype);
        }
    };

    function update(datatype) {
        var make_request = false;
        for (var element in elements) {
            if (elements[element].data_type == datatype) {
                elements[element].update();
                make_request = true;
            }
        }

        if (make_request) {
            websocketSend(datatype);
        }
    };

    function unregister(container_id) {
        var old_datatype = elements[container_id].data_type;
        types.splice(types.indexOf(old_datatype), 1);

        elements[container_id].destroy();
        delete elements[container_id];
    };

    function getType(container) {
        var parent = container.parent();
        if (parent.hasClass('sweep')) {
            return TYPE_SWEEP;
        }
        else {
            return parent.find('input[name=' + parent.attr('id') + '-type]:checked').val();
        }
    };

    function updateLimits() {
        if (!Visualisation.src_data || !Visualisation.rec_data) {
            return;
        }

        var min = 10 * Math.log(Math.min(math.min(Visualisation.src_data.data), math.min(Visualisation.rec_data.data))) / Math.log(10);
        var max = 10 * Math.log(Math.max(math.max(Visualisation.src_data.data), math.max(Visualisation.rec_data.data))) / Math.log(10);

        if (min < Visualisation.ymin) {
            Visualisation.ymin = min;
        }

        if (max > Visualisation.ymax) {
            Visualisation.ymax = max;
        }
    };

    /* WebSocket helper functions */

    function websocketInit() {
        if (_socket === null) {
            _socket = new WebSocket("ws://" + window.location.hostname + ":1337");

            _socket.addEventListener("open", function() {
                console.log("Connected to " + _socket.url);
            });
            _socket.addEventListener("message", function(event) {
                var container = JSON.parse(event.data);
                Visualisation[container.dtype] = container;
                updateLimits();
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

    function websocketSend(data) {
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

        init : function(wrapper_id) {
            if (!Visualisation.running()) {
                window.setTimeout(Visualisation.init, 100, wrapper_id);
                return;
            }

            var container = $("#" + wrapper_id + "-container");
            var type = getType(container);
            var datatype = $('input[name=' + wrapper_id + '-data]:checked', "#" + wrapper_id).val();
            container.html("");

            if (elements[wrapper_id]) {
                unregister(wrapper_id);
            }

            title(container, type, datatype);

            if (datatype == DATATYPE_DET_DATA) {
                elements[wrapper_id] = new DetPlot(wrapper_id);
                $("#" + wrapper_id + " .visualisation-type").find('input').prop('disabled', true);
            }
            else if (type == TYPE_NONE) {
                $("#" + wrapper_id + " .visualisation-data").find('input').prop('disabled', true);
            }
            else {
                if (type == TYPE_FFT) {
                    elements[wrapper_id] = new FFTplot(wrapper_id, datatype);
                }
                else if (type == TYPE_SPECTROGRAM) {
                    elements[wrapper_id] = new SpectroGram(wrapper_id, datatype);
                }
                else if (type == TYPE_SWEEP) {
                    elements[wrapper_id] = new Sweep(wrapper_id, datatype);
                }

                $("#" + wrapper_id + " .visualisation-type").find('input').prop('disabled', false);
                $("#" + wrapper_id + " .visualisation-data").find('input').prop('disabled', false);
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

