/**
 * Logic for rendering an FFT plot using highcharts.
 */

var FFTplot = function(container_id){
    this.N = 10;
    var that = this; // Because JS is retarded.

    // Add message listener.
    Connection.socket().addEventListener("message", function(e) { that.onMessage(e); });

    // Set up the chart.
    this.container_id = container_id;
    this.chart = new Highcharts.Chart(this.getPlotSettings());

    // Set up the averaging slider.
    this.averaging_slider = $("#" + container_id + "-averaging-slider").slider();
    this.averaging_slider.slider("setValue", this.N);
    $(document).on("change", "#" + container_id + "-averaging-slider", function() {
        that.N = parseInt(this.value);
    });
};

FFTplot.prototype.onMessage = function(event) {
    if (typeof event.data == 'string' || event.data instanceof String) {
        // Parse the message content.
        var response = JSON.parse(event.data);
        var sample_freq = response.sample_freq;
        var center_freq = response.center_freq;
        var fft_data = response.data;

        // Update the chart
        this.averaged_fft = this.getAverage(fft_data);

        fft_data = math.log10(this.averaged_fft);
        fft_data = math.multiply(fft_data, 10);
        this.chart.series[0].setData(fft_data);
        this.fixAxes(fft_data, sample_freq, center_freq);
    } else {
        console.log("Received unsupported message type.");
    }
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
            renderTo: this.container_id
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
            animation: false,
            turboThreshold: 2048
        }],
        tooltip: {
            enabled: false
        },
        credits: {
            enabled: false
        }
    };
};
