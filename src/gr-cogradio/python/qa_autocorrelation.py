from gnuradio import gr, gr_unittest
from gnuradio import blocks
from autocorrelation import autocorrelation


class qa_autocorrelation (gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    # def test_001_t(self):
    #     source_data = (1, 1)
    #     expected_result = (1, 1)
    #     source = blocks.vector_source_f(source_data)
    #     rx = autocorrelation(2, 1)
    #     sink = blocks.vector_sink_f()
    #     self.tb.connect(source, rx)
    #     self.tb.connect(rx, sink)

    #     self.tb.run()
    #     result_data = sink.data()

    #     self.assertFloatTuplesAlmostEqual(expected_result, result_data, 2)


if __name__ == '__main__':
    gr_unittest.run(qa_autocorrelation, "qa_autocorrelation.xml")
