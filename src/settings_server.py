#!/usr/bin/env python
import Pyro4
import cogradio_vis as vis
from multiprocessing import Process


def settings_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    settings = vis.settings.Settings()
    uri = daemon.register(settings)
    ns.register("cg.settings", uri)
    daemon.requestLoop()


def safe_start_name_server():
    try:
        Pyro4.locateNS()
    except Pyro4.errors.NamingError:
        print "Starting naming server"
        p = Process(target=Pyro4.naming.startNSloop)
        p.start()


if __name__ == "__main__":
    safe_start_name_server()
    settings_server()
