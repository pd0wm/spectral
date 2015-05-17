var SpectroGram = function(container_id) {
    this.initCanvas(container_id);

    if (!Connection.isOpen()) {
        Connection.hostname = window.location.hostname;
        Connection.open();
        var that = this;
    }
    Connection.socket().addEventListener("message", function(e) { that.onMessage(e); });

    this.colormap = chroma.scale(
        ['#FFF', Highcharts.getOptions().colors[0], "#1981E6", "#043361"]
    ).mode('rgb');
}

SpectroGram.prototype.onMessage = function(event) {
    if (typeof event.data == 'string' || event.data instanceof String) {
        var response = JSON.parse(event.data);
        var sample_freq = response.sample_freq;
        var fft_data = response.data;

        this.draw(fft_data);
    }
    else {
        console.log("Received unsupported message type.");
    }
};

SpectroGram.prototype.initCanvas = function(container_id) {
    this.canvas = document.getElementById(container_id);
    this.canvas.width = this.canvas.clientWidth;
    this.canvas.height = this.canvas.clientHeight;
    this.ctx = this.canvas.getContext("2d");
};

SpectroGram.prototype.draw = function(fft_data) {
    var temp_canvas = this.ctx.canvas;
    this.ctx.translate(0, -1);
    this.ctx.drawImage(temp_canvas, 0, 0);
    this.ctx.resetTransform();

    var max = math.max(fft_data);
    var fft_data_scaled = this.rescale(fft_data, this.canvas.width)

    for (var i = 0; i < this.canvas.width; i++) {
        this.ctx.fillStyle = this.colormap(fft_data_scaled[i] / max);
        this.ctx.fillRect(i, this.canvas.height - 1, 1, 1);
    }
};

SpectroGram.prototype.rescale = function(fft_data, length) {
    if (fft_data.length > length) {
        return this.downscale(fft_data, length);
    }

    if (fft_data.length < length) {
        return this.upscale(fft_data, length);
    }

    return fft_data;
};

SpectroGram.prototype.upscale = function(fft_data, length) {
    var fft_data_scaled = new Array(length);
    var binsize = Math.round(length / fft_data.length);
    var delta_err = binsize * fft_data.length / length;
    var err = 0;
    var j = 0;

    for (var i = 0; i < length; i++) {
        fft_data_scaled[i++] = fft_data[j];
        err += delta_err;

        while (err >= 0.5) {
            fft_data_scaled[i] = fft_data[j++];
            err--;
        }
    }

    return fft_data_scaled;
};

SpectroGram.prototype.downscale = function(fft_data, length) {
    var fft_data_scaled = new Array(length);
    var binsize = Math.round(length / fft_data.length);
    var delta_err = binsize * fft_data.length / length;
    var err = 0;
    var j = 0;

    for (var i = 0; i < length; i++) {
        var tmp_j = j;
        var data = 0;
        err += delta_err;

        while (err >= 0.5) {
            data += fft_data[j++];
            err--;
        }

        fft_data_scaled[i] = data / (j - tmp_j);
    }

    return fft_data_scaled;
};
