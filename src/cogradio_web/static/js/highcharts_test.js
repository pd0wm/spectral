var chart;
var length;
var current_fft;
var REQUEST_DATA = 0;
var N;
var buffer;
var filter;

document.addEventListener("socket_open", function(e){ subscribe(); });

$(document).ready(function() {
    connection.hostname = window.location.hostname;
    connection.open();
    $('#slider-N').slider();
    N = parseInt(document.getElementById("slider-N").value);
});

$(document).on("change", "#slider-N", function() {
    N = parseInt(this.value);
    initBuffer(current_fft);
});

function onClose (event) {

}

function onMessage (event) {
    if (typeof event.data == 'string' || event.data instanceof String) {
        var data = JSON.parse(event.data);
        fft = data.data;
        length = fft.length;
        var sample_freq = data.sample_freq;

        chart = $('#container').highcharts();
        current_fft = getAverage(fft);

        chart.series[0].setData(current_fft);
        connection.send(REQUEST_DATA);

        fixAxes(current_fft, sample_freq);
    }
}

function subscribe() {
    connection.socket().addEventListener("close", function(event) { onClose(event); });
    connection.socket().addEventListener("message", function(event) { onMessage(event); });
    connection.socket().addEventListener("error", function(event) { onError(event); });
}

$(function () {
    $('#container').highcharts({
        chart: {
            zoomType: 'x',
            animation: false,
        },
        title: {
            text: 'Real-time FFT'
        },
        xAxis: {
            type: 'linear',
            title: { text: 'Frequency [Hz]' }
        },
        yAxis: {
            max: 0,
            min: 0,
            title: { text: '' }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    enabled: false
                },
                lineWidth: 1,
                threshold: null,
                enableMouseTracking: false
            }
        },
        series: [{
            type: 'area',
            name: 'FFT',
        }],
        tooltip: {
            enabled: false
        }
    });
});

function fixAxes(data, sample_freq) {
    var interval = sample_freq / data.length;

    if (chart.series[0].pointInterval != interval) {
        chart.series[0].update({
            pointInterval: interval,
            pointStart: -sample_freq / 2
        });
    }

    var ymax = Math.max.apply(Math, data);
    if (chart.yAxis[0].max < ymax) {
        chart.yAxis[0].update({max: ymax});
    }
}

function initBuffer(data) {
    buffer = math.zeros(N, length);

    for (var i = 0; i < N; i++){
        buffer._data[i] = data;
    }

    filter = math.multiply(math.ones(N), 1 / N);
}

function getAverage(data) {
    if (!buffer) {
        initBuffer(data);
    }

    buffer._data.shift();
    buffer._data.push(data);

    return math.multiply(filter, buffer)._data;
}
