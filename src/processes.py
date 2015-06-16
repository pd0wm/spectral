import cogradio as cg
import cogradio_vis as vis


def run_generator(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor):
    settings = vis.get_settings_object()
    while True:
        source.parse_options(settings.read())

        orig_signal = source.generate(block_size)
        sampled = sampler.sample(orig_signal)
        signal_queue.queue(sampled)

        offset = int(block_size / upscale_factor)
        data = cg.fft(cg.auto_correlation(orig_signal, maxlag=offset))

        vis.send_to_websocket(websocket_src_queue, data, vis.websocket.ServerProtocolData.SRC_DATA)


def run_reconstructor(signal_queue, websocket_rec_queue, det_queue, reconstructor, sample_freq):
    while True:
        inp = signal_queue.dequeue()
        if inp is not None:
            rx = reconstructor.reconstruct(inp)
            signal = cg.fft(rx)
            det_queue.queue(rx)
            vis.send_to_websocket(websocket_rec_queue, signal, vis.websocket.ServerProtocolData.REC_DATA)


def run_detector(detector, detection_queue, websocket_det_queue):
    settings = vis.get_settings_object()
    while True:
        detector.parse_options(settings.read())
        inp = detection_queue.dequeue()
        if inp is not None:
            detect = [int(x) for x in detector.detect(inp)]
            vis.send_to_websocket(websocket_det_queue, detect, vis.websocket.ServerProtocolData.DET_DATA)


def run_server():
    vis.webserver.flaskr.app.run(host='0.0.0.0', use_reloader=False)


def run_websocket_data(data_port, web_src_queue, web_rec_queue, web_det_queue, sample_freq):
    vis.websocket_data(data_port, web_src_queue, web_rec_queue, web_det_queue, sample_freq)


def run_websocket_control(port):
    vis.websocket_control(port)
