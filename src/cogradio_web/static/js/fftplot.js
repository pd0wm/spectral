var FFTplot = function(container_id){
    this.N = 10;
    this.REQUEST_DATA = 0;

    if (!Connection.isOpen()) {
        Connection.hostname = window.location.hostname;
        Connection.open();
        var that = this;
    }
    Connection.socket().addEventListener("message", function(e) { that.onMessage(e); });

    this.container_id = container_id;
    this.chart = new Highcharts.Chart(this.getPlotSettings());

    this.averaging_slider = $("#" + container_id + "-averaging-slider").slider();
    this.averaging_slider.slider("setValue", this.N);
    $(document).on("change", "#" + container_id + "-averaging-slider", function() {
        that.N = parseInt(this.value);
    });
};

FFTplot.prototype.onMessage = function(event) {
    if (typeof event.data == 'string' || event.data instanceof String) {
        var response = JSON.parse(event.data);
        var sample_freq = response.sample_freq;
        var fft_data = response.data;

        this.averaged_fft = this.getAverage(fft_data);
        this.chart.series[0].setData(this.averaged_fft);
        this.fixAxes(this.averaged_fft, sample_freq);

        Connection.send(this.REQUEST_DATA);
    } else {
        console.log("Received unsupported message type.");
    }
};

FFTplot.prototype.getAverage = function(fft_data) {
    if (!this.buffer || this.buffer.size()[0] != this.N) {
        if (!this.averaged_fft) {
            this.averaged_fft = fft_data;
        }

        this.initBuffer(fft_data.length);
    }

    this.buffer._data.shift();
    this.buffer._data.push(fft_data);

    return math.log10(math.multiply(this.filter, this.buffer)._data);
};

FFTplot.prototype.initBuffer = function(length) {
    this.buffer = math.zeros(this.N, length);

    for (var i = 0; i < this.N; i++){
        this.buffer._data[i] = this.averaged_fft;
    }

    this.filter = math.multiply(math.ones(this.N), 1 / this.N);
};

FFTplot.prototype.fixAxes = function(fft_data, sample_freq) {
    var interval = sample_freq / fft_data.length;

    if (this.chart.series[0].pointInterval != interval) {
        this.chart.series[0].update({
            pointInterval: interval,
            pointStart: -sample_freq / 2
        });
    }

    var ymax = Math.max.apply(Math, fft_data);
    if (this.chart.yAxis[0].max < ymax) {
        this.chart.yAxis[0].update({max: ymax});
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
        }],
        tooltip: {
            enabled: false
        }
    };
};
