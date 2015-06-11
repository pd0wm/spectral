/**
 * Logic for rendering an FFT plot using highcharts.
 */

var DetPlot = function(wrapper_id) {
    this.wrapper_id = wrapper_id;
    this.container_id = wrapper_id + "-container";
    this.data_type = 'det_data';

    // Set up the chart.
    this.chart = new Highcharts.Chart(this.getPlotSettings());
};

DetPlot.prototype.update = function() {
    // Parse the message content.
    var sample_freq = Visualisation[this.data_type].sample_freq;
    var center_freq = Visualisation[this.data_type].center_freq;
    var fft_data = Visualisation[this.data_type].data;

    // Update the chart
    this.chart.series[0].setData(fft_data, false, false, true);
    this.fixAxes(fft_data, sample_freq, center_freq);
    this.chart.redraw();
};

DetPlot.prototype.fixAxes = function(fft_data, sample_freq, center_freq) {
    // Fix horizontal scale when needed.
    var interval = sample_freq / fft_data.length;
    var prev_interval = this.chart.series[0].pointInterval;
    var point_start = center_freq - sample_freq / 2;
    var prev_point_start = this.chart.series[0].xData[0];

    if (prev_interval != interval || prev_point_start != point_start) {
        this.chart.series[0].update({
            pointInterval: interval,
            pointStart: point_start
        });
    }
};

DetPlot.prototype.getPlotSettings = function() {
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
            tickPositions: [0, 1, 2],
            title: { text: 'Signal detected [yes/no]' }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            column: {
                enableMouseTracking: false,
                animation: false,
                turboThreshold: 10000,
                groupPadding: 0,
                pointPadding: 0,
                borderWidth: 0,
            }
        },
        series: [{
            animation: false,
            type: 'column',
        }],
        tooltip: {
            enabled: false
        },
        credits: {
            enabled: false
        }
    };
};

DetPlot.prototype.destroy = function() {
    this.chart.destroy();
};
