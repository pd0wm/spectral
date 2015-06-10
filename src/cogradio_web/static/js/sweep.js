/**
 * Logic for rendering an FFT plot using highcharts.
 */

 var Sweep = function(container_id){
    this.container_id = container_id;
    this.data_type = 'rec_data';

    // Set up the chart.
    this.container_id = container_id;
    this.chart = new Highcharts.Chart(this.getPlotSettings());
};

FFTplot.prototype.update = function() {
    // Parse the message content.
    var sample_freq = Visualisation[this.data_type].sample_freq;
    var center_freq = Visualisation[this.data_type].center_freq;
    var fft_data = Visualisation[this.data_type].data;

    fft_data = math.log10(fft_data);
    fft_data = math.multiply(fft_data, 10);
};

FFTplot.prototype.fixAxes = function(fft_data, sample_freq, center_freq) {
    // Fix horizontal scale when needed.
    var interval = sample_freq / fft_data.length;
    var prev_interval = this.chart.series[0].pointInterval;
    var point_start = -sample_freq / 2 + center_freq;
    var prev_point_start = this.chart.series[0].pointStart;

    if (prev_interval != interval || prev_point_start != point_start) {
        this.chart.series[0].update({
            pointInterval: interval,
            pointStart: point_start
        });
    }

    var ymax = math.max(fft_data);
    if (this.chart.yAxis[0].max < ymax) {
        this.chart.yAxis[0].update({max: ymax});
    }

    var ymin = math.min(fft_data);
    if (this.chart.yAxis[0].min > ymin) {
        this.chart.yAxis[0].update({min: ymin});
    }
};

FFTplot.prototype.getPlotSettings = function() {
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
            animation: false,
            turboThreshold: 1200
        }],
        tooltip: {
            enabled: false
        },
        credits: {
            enabled: false
        }
    };
};

FFTplot.prototype.destroy = function() {
    this.chart.destroy();
};
