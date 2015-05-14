var chart;
var REQUEST_DATA = 0;

document.addEventListener("socket_open", function(e){ subscribe(); });

$(document).ready(function() {
    connection.hostname = window.location.hostname;
    connection.open();
});

function onClose (event) {

}

function onMessage (event) {
    if (typeof event.data == 'string' || event.data instanceof String) {
        var data = JSON.parse(event.data);
        chart = $('#container').highcharts();
        chart.series[0].setData(data.data);
        connection.send(REQUEST_DATA);

        fixAxes(data);
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

function fixAxes(data) {
    var interval = data.sample_freq / data.data.length;

    if (chart.series[0].pointInterval != interval) {
        chart.series[0].update({
            pointInterval: interval,
            pointStart: -data.sample_freq / 2
        });
    }

    var ymax = Math.max.apply(Math, data.data);
    if (chart.yAxis[0].max < ymax) {
        chart.yAxis[0].update({max: ymax});
    }
}
