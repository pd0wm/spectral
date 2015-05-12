var socket;
var output;
var toggleButton;
var samplerate = 32000;
var chart;

$(document).ready(function() {
    output = document.getElementById("output");
    toggleButton = document.getElementById("toggleButton");
});

function onOpen (event) {
    writeLine('Connected to: ' + socket.url);
    toggleButton.innerHTML = "Disconnect";
}

function onClose (event) {
    writeLine('Closed connection');
    toggleButton.innerHTML = "Connect";
}

function onMessage (event) {
    if (typeof event.data == 'string' || event.data instanceof String) {
        writeLine('Received message: ' + event.data);
        chart = $('#container').highcharts();
        chart.series[0].setData(JSON.parse(event.data));
    }
    else{
        writeLine('Received binary message');
    }
}

function onError (event) {
    writeLine('Error: ', event.data);
}

function toggleConnect() {
    if (socket instanceof WebSocket && socket.readyState == WebSocket.OPEN) {
        disconnect();
    }
    else {
        connect();
    }
}

function connect() {
    socket = new WebSocket("ws://127.0.0.1:9000");
    socket.onopen = function(event) { onOpen(event) };
    socket.onclose = function(event) { onClose(event) };
    socket.onmessage = function(event) { onMessage(event) };
    socket.onerror = function(event) { onError(event) };
}

function disconnect() {
    socket.close(1000, 'User closed connection');
}

function writeLine(line) {
    output.value += line + "\n";
}

window.addEventListener("load", "init()", false);

$(function () {
    $('#container').highcharts({
        chart: {
            zoomType: 'x'
        },
        title: {
            text: 'FFT test plot'
        },
        xAxis: {
            type: 'linear',
            // minRange: -samplerate / 2,
            // maxRange: samplerate / 2
        },
        yAxis: {
            title: {
                text: ''
            }
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
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },
        series: [{
            type: 'area',
            name: 'FFT',
            pointInterval: 1,
            // pointStart: -samplerate / 2,
            // pointEnd: samplerate / 2,
            data: [
                0.8446, 0.8445, 0.8444, 0.8451, 0.8418, 0.8264, 0.8258, 0.8232, 0.8233, 0.8258
            ]
        }]
    });
});
