/**
 * Logic for rendering a spectrogram using an HTML5 canvas.
 */

var SpectroGram = function(container_id) {
    this.initCanvas(container_id);

    var that = this;
    Connection.socket().addEventListener("message", function(e) { that.onMessage(e); });

    this.colormap = chroma.scale(['#FFF', '#CCC', Highcharts.getOptions().colors[0]]);
    // this.colormap = chroma.scale(["#000", "#F00", "#FF0", "#FFF"]);
};

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

    // Reset transform not supported by safari, so manual reset with identity matrix
    this.ctx.setTransform(1, 0, 0, 1, 0, 0);

    var fft_data_scaled = math.log10(this.rescale(fft_data, this.canvas.width));
    var min = math.min(fft_data_scaled);
    fft_data_scaled = math.add(math.abs(min), fft_data_scaled);
    var max = math.max(fft_data_scaled);

    for (var i = 0; i < this.canvas.width; i++) {
        this.ctx.fillStyle = this.colormap(fft_data_scaled[i] / max).hex();
        this.ctx.fillRect(i, this.canvas.height - 1, 1, 1);
    }
};

SpectroGram.prototype.rescale = function(fft_data, length) {
    // Create a new array to fit the amount of pixels to render.
    if (fft_data.length > length) {
        return this.downscale(fft_data, length);
    }

    if (fft_data.length < length) {
        return this.upscale(fft_data, length);
    }

    return fft_data;
};

SpectroGram.prototype.upscale = function(fft_data, length) {
    // Create a new, longer array from the data in the given array,
    // using a method derived from Bresenham's line algorithm.
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
    // Create a new, shorter array from the data in the given array,
    // using a method derived from Bresenham's line algorithm.
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
