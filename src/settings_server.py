#!/usr/bin/env python
import Pyro4
import spectral.supervisor as ss
from multiprocessing import Process


def settings_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    settings = ss.settings.Settings()
    uri = daemon.register(settings)
    ns.register("sc.settings", uri)
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
