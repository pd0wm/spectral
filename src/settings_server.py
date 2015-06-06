#!/usr/bin/env python
import Pyro4
import cogradio as cg


def settings_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    settings = cg.Settings()
    uri = daemon.register(settings)
    ns.register("cg.settings", uri)
    daemon.requestLoop()


if __name__ == "__main__":
    settings_server()
