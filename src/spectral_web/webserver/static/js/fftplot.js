/**
 * Logic for rendering an FFT plot using highcharts.
 */

var FFTplot = function(wrapper_id, data_type){
    this.N = 10;
    this.wrapper_id = wrapper_id;
    this.container_id = wrapper_id + "-container";
    this.data_type = data_type;

    // Set up the chart.
    this.chart = new Highcharts.Chart(this.getPlotSettings());

    // Set up the averaging slider.
    $("#" + this.container_id).append(this.getSliderHtml());
    this.averaging_slider = $("#" + this.wrapper_id + "-averaging-slider").slider();
    this.averaging_slider.slider("setValue", this.N);
    $(document).on("change", "#" + this.wrapper_id + "-averaging-slider", {plotter: this}, function(e) {
        e.data.plotter.N = parseInt(this.value);
    });
};

FFTplot.prototype.getType = function() {
    var parent = container.parent();
    if (parent.hasClass('sweep')) {
        return TYPE_SWEEP;
    }
    else {
        return parent.find('input[name=' + parent.attr('id') + '-type]:checked').val();
    }
};

FFTplot.prototype.update = function() {
    // Parse the message content.
    var sample_freq = Visualisation[this.data_type].sample_freq;
    var center_freq = Visualisation[this.data_type].center_freq;
    var fft_data = Visualisation[this.data_type].data;

    // Update the chart
    this.averaged_fft = this.getAverage(fft_data);

    fft_data = math.log10(this.averaged_fft);
    fft_data = math.multiply(fft_data, 10);
    this.chart.series[0].setData(fft_data, false, false, true);
    this.fixAxes(fft_data, sample_freq, center_freq);
    this.chart.redraw();
};

FFTplot.prototype.getAverage = function(fft_data) {
    if (this.N == 1) {
        return fft_data;
    }

    // If buffer does not exist or is of the wrong size, initialise.
    if (!this.buffer || this.buffer.size()[0] != this.N) {
        if (!this.averaged_fft) {
            this.averaged_fft = fft_data;
        }

        this.initBuffer(fft_data.length);
    }

    // Put in the new data, return the new average.
    this.buffer._data.shift();
    this.buffer._data.push(fft_data);

    return math.multiply(this.filter, this.buffer)._data;
};

FFTplot.prototype.initBuffer = function(length) {
    this.buffer = math.zeros(this.N, length);

    for (var i = 0; i < this.N; i++){
        this.buffer._data[i] = this.averaged_fft;
    }

    this.filter = math.multiply(math.ones(this.N), 1 / this.N);
};

FFTplot.prototype.fixAxes = function(fft_data, sample_freq, center_freq) {
    // Fix horizontal scale when needed.
    var interval = sample_freq / fft_data.length;
    var prev_interval = this.chart.series[0].pointInterval;
    var point_start = -sample_freq / 2 + center_freq;
    var prev_point_start = this.chart.series[0].xData[0];

    if (prev_interval != interval || prev_point_start != point_start) {
        this.chart.series[0].update({
            pointInterval: interval,
            pointStart: point_start
        });
    }

    if (this.chart.yAxis[0].max < Visualisation.ymax) {
        this.chart.yAxis[0].update({max: Visualisation.ymax});
    }

    if (this.chart.yAxis[0].min > Visualisation.ymin) {
        this.chart.yAxis[0].update({min: Visualisation.ymin});
    }
};

FFTplot.prototype.getPlotSettings = function() {
    return {
        chart: {
            animation: false,
            height: 400,
            renderTo: this.container_id,
            zoomType: 'x'
        },
        title: {
            text: null
        },
        xAxis: {
            title: { text: 'Frequency [Hz]' },
            type: 'linear'
        },
        yAxis: {
            max: 0,
            min: 0,
            title: { text: '[dB]' }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                animation: false,
                enableMouseTracking: false,
                fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                lineWidth: 1,
                marker: {
                    enabled: false
                },
                threshold: null
            }
        },
        series: [{
            animation: false,
            name: 'FFT',
            turboThreshold: 10000,
            type: 'area'
        }],
        tooltip: {
            enabled: false
        },
        credits: {
            enabled: false
        }
    };
};

FFTplot.prototype.getSliderHtml = function() {
    return '<div> \
        <h3 class="panel-title" style="text-align: center; margin-bottom:0.5em;">Averaging</h3> \
        <input id="' + this.wrapper_id + '-averaging-slider" type="text" style="width: 100%;" data-slider-min="1" data-slider-max="20" data-slider-step="1" data-slider-orientation="horizontal" data-slider-selection="after" data-slider-tooltip="show"> \
    </div>';
}

FFTplot.prototype.destroy = function() {
    this.chart.destroy();
};
