import numpy as np
import plotly.graph_objects as go
import quandl
import matplotlib.dates as dates
import plotly.io as pio
import pandas as pd
from datetime import datetime

data = quandl.get('USTREASURY/YIELD', returns='numpy', trim_start="2022-06-01")
header = [float(name.split(" ")[0]) / (12 if name.split(" ")[1] == 'Mo' else 1) for name in data.dtype.names[1:]]

x_data = [[pd.to_datetime(dt).strftime('%Y%m%d') for i in range(len(data.dtype.names)-1)] for dt in data.Date]
y_data = [header] * len(data)
z_data = [list(row.tolist()[1:]) for row in data]

x = np.array(x_data, dtype='str')
y = np.array(y_data, dtype='f')
z = np.array(z_data, dtype='f')

pio.renderers.default = 'browser'

fig = go.Figure()

# Linear scale surface plot
fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Inferno', showscale=True, name='Linear'))

# Log scale surface plot
fig.add_trace(go.Surface(x=x, y=np.log10(y), z=z, colorscale='Inferno', showscale=True, name='Log', visible=False))

fig.update_layout(
    title='US Treasury Yield Curve',
    scene=dict(
        xaxis_title='Date (YYYYMMDD)',
        yaxis_title='Maturity（償還年数）',
        zaxis_title='Yield'
    ),
    autosize=True,
    margin=dict(l=0, r=0, t=60, b=0),
    font=dict(size=14),
    updatemenus=[
        dict(
            type='buttons',
            showactive=True,
            buttons=[
                dict(label='Linear', method='update', args=[{'visible': [True, False]}, {'title': 'US Treasury Yield Curve (Linear)'}]),
                dict(label='Log', method='update', args=[{'visible': [False, True]}, {'title': 'US Treasury Yield Curve (Log)'}]),
            ],
        )
    ],
)

fig.update_xaxes(automargin=True)
fig.update_yaxes(automargin=True)

fig.write_html(
    './docs/index.html',
    config={'responsive': True},
    include_plotlyjs='cdn',
    full_html=False
)

# fig.show()
