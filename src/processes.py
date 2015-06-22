import spectral.core as sc
import spectral.supervisor as ss
import spectral.web as sw


def run_generator(signal_queue, websocket_src_queue, source, sampler, sample_freq, block_size, upscale_factor):
    settings = ss.get_settings_object()
    while True:
        source.parse_options(settings.read())

        orig_signal = source.generate(block_size)
        sampled = sampler.sample(orig_signal)
        signal_queue.queue(sampled)

        offset = int(block_size / upscale_factor)
        data = sc.fft(sc.auto_correlation(orig_signal, maxlag=offset))

        ss.send_to_websocket(websocket_src_queue, data, ss.websocket.ServerProtocolData.SRC_DATA)


def run_reconstructor(signal_queue, websocket_rec_queue, det_queue, reconstructor, sample_freq):
    while True:
        inp = signal_queue.dequeue()
        if inp is not None:
            rx = reconstructor.reconstruct(inp)
            signal = sc.fft(rx)
            det_queue.queue(rx)
            ss.send_to_websocket(websocket_rec_queue, signal, ss.websocket.ServerProtocolData.REC_DATA)


def run_detector(detector, detection_queue, websocket_det_queue):
    settings = ss.get_settings_object()
    while True:
        detector.parse_options(settings.read())
        inp = detection_queue.dequeue()
        if inp is not None:
            detect = [int(x) for x in detector.detect(inp)]
            ss.send_to_websocket(websocket_det_queue, detect, ss.websocket.ServerProtocolData.DET_DATA)


def run_server():
    sw.webserver.flaskr.app.run(host='0.0.0.0', use_reloader=False)


def run_websocket_data(data_port, web_src_queue, web_rec_queue, web_det_queue, sample_freq):
    ss.websocket_data(data_port, web_src_queue, web_rec_queue, web_det_queue, sample_freq)


def run_websocket_control(port):
    ss.websocket_control(port)
