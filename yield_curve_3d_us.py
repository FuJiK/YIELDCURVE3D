# %%
import numpy as np
import plotly.graph_objects as go
import quandl
import matplotlib.dates as dates
# Import additional libraries
import plotly.io as pio
import pandas as pd
from datetime import datetime

# %%
# Fetch data from Quandl
data = quandl.get('USTREASURY/YIELD', returns='numpy', trim_start="2022-06-01")

# %%
# Convert header to float
header = [float(name.split(" ")[0]) / (12 if name.split(" ")[1] == 'Mo' else 1) for name in data.dtype.names[1:]]



# %%
# Extract x, y, and z data
# Convert x_data to string format
x_data = [[pd.to_datetime(dt).strftime('%Y%m%d') for i in range(len(data.dtype.names)-1)] for dt in data.Date]
#x_data
# x_data = [[dates.date2num(dt) for i in range(len(data.dtype.names)-1)] for dt in data.Date]
y_data = [header] * len(data)
z_data = [list(row.tolist()[1:]) for row in data]

# %%
# Build numpy arrays
x = np.array(x_data, dtype='str')
# x = np.array(x_data, dtype='f')
y = np.array(y_data, dtype='f')
z = np.array(z_data, dtype='f')

# Set default renderer to "browser" to use the full-featured plotly.js library
pio.renderers.default = 'browser'

# # %%
# # Create a 3D surface plot
# fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Inferno', showscale=True)])

# fig.update_layout(title='US Treasury Yield Curve', scene=dict(
#     xaxis_title='Term',
#     yaxis_title='Maturity',
#     zaxis_title='Yield'
# ))

# # %%
# # Save the figure as an HTML file
# fig.write_html('./docs/index.html')

# Create a 3D surface plot
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

# Configure the plot to be responsive
fig.update_xaxes(automargin=True)
fig.update_yaxes(automargin=True)

# Save the figure as an HTML file with responsive settings
fig.write_html(
    './docs/index.html',
    config={'responsive': True},
    include_plotlyjs='cdn',  # Use Plotly.js CDN for smaller file size
    full_html=False  # Remove HTML header and footer to reduce file size and improve loading speed
)

# %%
# Show the figure in the notebook (optional)
# fig.show()


