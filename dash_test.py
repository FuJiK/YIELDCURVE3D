import numpy as np
import plotly.graph_objects as go
import quandl
import pandas as pd
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Checklist(
        id='maturity-checklist',
        options=[{'label': f'{maturity} Yr', 'value': i} for i, maturity in enumerate(header)],
        value=list(range(len(header))),
        inline=True
    ),
    dcc.Graph(id='yield-curve'),
])

# Define the callback
@app.callback(
    Output('yield-curve', 'figure'),
    [Input('maturity-checklist', 'value')]
)
def update_figure(selected_maturities):
    # Create a 3D surface plot
    fig = go.Figure()

    # Create Surface traces for each Maturity
    for i, maturity in enumerate(header):
        if i in selected_maturities:
            fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Inferno', showscale=True, name=f'{maturity} Yr', visible=True))

    # Update layout
    fig.update_layout(
        title='US Treasury Yield Curve',
        scene=dict(
            xaxis_title='Date (YYYYMMDD)',
            yaxis_title='Maturity',
            zaxis_title='Yield'
        ),
    )

    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True,port=59674)
