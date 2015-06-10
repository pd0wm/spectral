#!/usr/bin/env python
import sys
from multiprocessing import Process, Queue
from twisted.internet import reactor
from twisted.python import log
from cogradio_web import app, WebSocketServerDashFactory, ServerProtocolDash

port = 1337


def run_server():
    app.run(host='0.0.0.0', use_reloader=False)


def run_websocket_server():
    log.startLogging(sys.stdout)
    factory = WebSocketServerDashFactory(url="ws://localhost:{}".format(port))
    factory.protocol = ServerProtocolDash
    reactor.listenTCP(port, factory)
    reactor.run()

if __name__ == '__main__':
    p1 = Process(target=run_server,
                 args=())
    p2 = Process(target=run_websocket_server,
                 args=())
    processes = [p1, p2]

    try:
        [p.start() for p in processes]
        [p.join() for p in processes]
    except KeyboardInterrupt:
        flag = True
        while flag:
            flag = False
            for p in processes:
                if p.is_alive():
                    flag = True
                    p.terminate()
                    print p, "termination sent"
            time.sleep(1)
    finally:
        sys.exit(1)
