/**
 * Logic for rendering a spectrogram using an HTML5 canvas.
 */

var SpectroGram = function(wrapper_id, data_type) {
    this.wrapper_id = wrapper_id;
    this.container_id = wrapper_id + "-container";
    this.initCanvas(wrapper_id);
    this.data_type = data_type;

    this.colormap = chroma.scale(['#FFF', '#CCC', Highcharts.getOptions().colors[0]]);
};

SpectroGram.prototype.update = function() {
    var sample_freq = Visualisation[this.data_type].sample_freq;
    var fft_data = Visualisation[this.data_type].data;

    this.draw(fft_data);
};

SpectroGram.prototype.initCanvas = function() {
    var container = $("#" + this.container_id).append(
        '<canvas id="' + this.wrapper_id +'-spectrogram" style="width:100%; height:400px;"></canvas>'
    );

    this.canvas = container.children("canvas").get(0);
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
    // Create a new, longer array from the data in the given array.
    var fft_data_scaled = new Array(length);
    var fft_data_length = fft_data.length;

    for (i = 0; i < length; i++) {
        fft_data_scaled[i] = fft_data[Math.round(parseFloat(i)/length*(fft_data_length-1))];
    }

    return fft_data_scaled;
};

SpectroGram.prototype.destroy = function() {

};
