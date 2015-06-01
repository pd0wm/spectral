/**
 * Handles everything related to visualisation.
 */

var Visualisation = function() {
    var TYPE_NONE = 'none';
    var TYPE_FFT = 'fft';
    var TYPE_SPECTROGRAM = 'spectrogram'
    var TYPE_DET = 'detector'
    var DATATYPE_SRC_DATA = 'src_data';
    var DATATYPE_REC_DATA = 'rec_data';
    var DATATYPE_DET_DATA = 'det_data';
    var title1 =
    {
        "none": 'N/A',
        "fft": 'FFT plot: ',
        "spectrogram": 'Spectrogram: '
    }
    var title2 =
    {
        'src_data': "original data",
        'rec_data': "reconstructed data",
        'det_data': "detection data",
    }
    var elements = {};
    var types  = [];

    function title(container, type, datatype) {
        var title = title1[type] + (type == TYPE_NONE ? "" : title2[datatype]);
        container.siblings("h3").text(title);
    }

    function register(datatype) {
        document.addEventListener(datatype, update_handler);

        if (Connection.isOpen()) {
            Connection.send(datatype);
        }
        else {
            Connection.socket().addEventListener("open", function() {
                Connection.send(datatype);
                Connection.socket().removeEventListener(datatype, arguments.callee);
            });
        }
    }

    function unregister(container_id) {
        var old_datatype = elements[container_id].data_type;
        types.splice(types.indexOf(old_datatype), 1);

        elements[container_id].destroy();
        delete elements[container_id];

        if (types.indexOf(old_datatype) == -1) {
            document.removeEventListener(old_datatype, update_handler);
        }
    }

    function update_handler(event) {
        Visualisation.update(event.type);
    };

    return {
        init : function(container_id) {
            var type = $('input[name=' + container_id + '-type]:checked', "#" + container_id).val()
            var datatype = $('input[name=' + container_id + '-data]:checked', "#" + container_id).val()
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
            else {
                if (type == TYPE_FFT) {
                    elements[container_id] = new FFTplot(container_id + "-container", datatype);
                }
                else if (type == TYPE_SPECTROGRAM) {
                    elements[container_id] = new SpectroGram(container_id + "-container", datatype);
                }

                $("#" + container_id + " .visualisation-type").find('input').prop('disabled', false);
            }


            if (type != TYPE_NONE) {
                if (types.indexOf(datatype) == -1) {
                    register(datatype);
                }

                types.push(datatype);
            }
        },
        update : function(datatype) {
            for (var element in elements) {
                if (elements[element].data_type == datatype) {
                    elements[element].update();
                }
            }
            Connection.send(datatype);
        }
    };
}();

