/**
 * Logic for rendering an FFT plot using highcharts.
 */

 var Sweep = function(wrapper_id, data_type, start, end) {
    this.wrapper_id = wrapper_id;
    this.container_id = wrapper_id + "-container";
    this.data_type = data_type;
    this.data = [];
    this.start = start;
    this.end = end;

    // Set up the chart.
    this.chart = new Highcharts.Chart(this.getPlotSettings());
};

Sweep.prototype.update = function() {
    // Parse the message content.
    var sample_freq = Visualisation[this.data_type].sample_freq;
    var center_freq = Visualisation[this.data_type].center_freq;
    var fft_data = math.multiply(math.log10(Visualisation[this.data_type].data));

    Array.prototype.push.apply(this.data, fft_data);
};

Sweep.prototype.fixAxes = function(fft_data, sample_freq, center_freq) {
    var ymax = math.max(fft_data);
    if (this.chart.yAxis[0].max < ymax) {
        this.chart.yAxis[0].update({max: ymax});
    }

    var ymin = math.min(fft_data);
    if (this.chart.yAxis[0].min > ymin) {
        this.chart.yAxis[0].update({min: ymin});
    }
};

Sweep.prototype.getPlotSettings = function() {
    return {
        chart: {
            zoomType: 'x',
            animation: false,
            renderTo: this.container_id,
            height: 400
        },
        title: {
            text: null
        },
        xAxis: {
            type: 'linear',
            title: { text: 'Frequency [Hz]' }
        },
        yAxis: {
            max: this.end,
            min: this.start,
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
            animation: false,
            turboThreshold: 1000000
        }],
        tooltip: {
            enabled: false
        },
        credits: {
            enabled: false
        }
    };
};

Sweep.prototype.destroy = function() {
    this.chart.destroy();
};
