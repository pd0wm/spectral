var socket;
var output;
var hostname;
var toggleButton;
var samplerate = 32000;
var chart;

$(document).ready(function() {
    hostname = document.getElementById("hostname");
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
        var data = JSON.parse(event.data);
        chart = $('#container').highcharts();
        chart.series[0].setData(JSON.parse(event.data));
        socket.send(1);

        fixAxes(data);
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
    socket = new WebSocket("ws://" + hostname.value + ":9000");
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
            zoomType: 'x',
            animation: false,
        },
        title: {
            text: 'FFT test plot'
        },
        xAxis: {
            type: 'linear',
            title: { text: 'Frequency [Hz]' }
        },
        yAxis: {
            max: 1000,
            min: 0
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
            pointStart: -samplerate / 2,
            data: []
        }]
    });
});

function fixAxes(data) {
    var interval = samplerate / data.length;

    if (chart.series[0].pointInterval != interval) {
        chart.series[0].update({pointInterval: interval});
    }

    var ymax = Math.max.apply(Math, data);
    if (chart.yAxis[0].max < ymax) {
        chart.yAxis[0].update({max: ymax});
    }
}
