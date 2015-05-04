from gnuradio import gr, gr_unittest
from gnuradio import blocks
from PSD import PSD


class qa_PSD (gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None


if __name__ == '__main__':
    gr_unittest.run(qs_PSD, "qa_PSD.xml")
