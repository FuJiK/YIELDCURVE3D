# %%
import numpy as np
import plotly.graph_objects as go
import quandl
import matplotlib.dates as dates

# %%
# Fetch data from Quandl
data = quandl.get('USTREASURY/YIELD', returns='numpy', trim_start="2022-06-01")

# %%
# Convert header to float
header = [float(name.split(" ")[0]) / (12 if name.split(" ")[1] == 'Mo' else 1) for name in data.dtype.names[1:]]

# %%
# Extract x, y, and z data
x_data = [[dates.date2num(dt) for i in range(len(data.dtype.names)-1)] for dt in data.Date]
y_data = [header] * len(data)
z_data = [list(row.tolist()[1:]) for row in data]

# %%
# Build numpy arrays
x = np.array(x_data, dtype='f')
y = np.array(y_data, dtype='f')
z = np.array(z_data, dtype='f')

# %%
# Create a 3D surface plot
fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Inferno', showscale=True)])

fig.update_layout(title='US Treasury Yield Curve', scene=dict(
    xaxis_title='Term',
    yaxis_title='Maturity',
    zaxis_title='Yield'
))

# %%
# Save the figure as an HTML file
fig.write_html('./dist/yield_curve_3d_us.html')

# %%
# Show the figure in the notebook (optional)
fig.show()


