import Pyro4


queue = Pyro4.Proxy("PYRONAME:jamqueue")

while True:
    rd = queue.read()
    if rd:
        print rd
    else:
        print
