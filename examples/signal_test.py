import plotly.plotly as py
from plotly.graph_objs import *
# auto sign-in with credentials or use py.sign_in()
trace1 = Scatter(
    x=[],
    y=[], 
    stream=dict(token='my_stream_id')
)
data = Data([trace1])
py.plot(data)
s = py.Stream('my_stream_id')
s.open()
s.write(dict(x=1, y=2))
s.close()
