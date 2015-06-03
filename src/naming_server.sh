export PYRO_SERIALIZERS_ACCEPTED=serpent,json,marshal,pickle
export PYRO_LOGFILE=pyro.log
export PYRO_LOGLEVEL=DEBUG
python2 -m Pyro4.naming &
