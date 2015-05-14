import gnuradio as gr


class UsrpN210(object):

    """Implementation of UsrpN210 driver"""

    def __init__(self, addr, channels=[0], cpu_format='fc32'):
        # Source.__init__(self)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("addr=192.168.10.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),)
