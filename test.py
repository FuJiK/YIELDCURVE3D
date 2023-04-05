import numpy as np
import plotly.graph_objects as go
import quandl
import pandas as pd
from datetime import datetime

# Fetch data from Quandl
data = quandl.get('USTREASURY/YIELD', returns='numpy', trim_start="2022-06-01")

# Convert header to float
header = [float(name.split(" ")[0]) / (12 if name.split(" ")[1] == 'Mo' else 1) for name in data.dtype.names[1:]]

# Extract x, y, and z data
# Convert x_data to string format
x_data = [[pd.to_datetime(dt).strftime('%Y%m%d') for i in range(len(data.dtype.names)-1)] for dt in data.Date]
y_data = [header] * len(data)
z_data = [list(row.tolist()[1:]) for row in data]

# Build numpy arrays
x = np.array(x_data, dtype='str')
y = np.array(y_data, dtype='f')
z = np.array(z_data, dtype='f')

# Create a 3D surface plot
fig = go.Figure()

# Create Surface traces for each Maturity and the Log scale
for maturity in header:
    fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Inferno', showscale=True, name=f'{maturity} Yr', visible=True))
    fig.add_trace(go.Surface(x=x, y=np.log10(y), z=z, colorscale='Inferno', showscale=True, name=f'{maturity} Yr (Log)', visible=False))

# Update layout
fig.update_layout(
    title='US Treasury Yield Curve',
    scene=dict(
        xaxis_title='Date (YYYYMMDD)',
        yaxis_title='Maturity',
        zaxis_title='Yield'
    ),
    updatemenus=[
        # Add a checklist for the Maturity on the left side
        dict(
            type='buttons',
            showactive=True,
            buttons=[
                dict(label='Linear', method='update', args=[{'visible': [True, False] * len(header)}, {'title': 'US Treasury Yield Curve (Linear)'}]),
                dict(label='Log', method='update', args=[{'visible': [False, True] * len(header)}, {'title': 'US Treasury Yield Curve (Log)'}]),
            ],
            x=1,
            xanchor='right',
            y=1,
            yanchor='top',
        ),
    ],
    updatemenudefaults=dict(showactive=True),
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

# Show the figure in the notebook (optional)
fig.show()
