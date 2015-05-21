import Pyro4

sets = {'h': 2, 'a': 4}
settings = Pyro4.Proxy("PYRONAME:cg.settings")
settings.update(sets)
print settings.get()
