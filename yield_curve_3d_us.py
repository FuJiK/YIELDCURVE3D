# %%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import quandl
import matplotlib.dates as dates
import matplotlib.ticker as ticker
from ipywidgets import interact

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
def plot_interactive_3d(elev=10, azim=270):
    fig = plt.figure(figsize=(30, 20))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(x, y, z, rstride=50, cstride=1, cmap='inferno', vmin=np.nanmin(z), vmax=np.nanmax(z))

    ax.set_title('US Treasury Yield Curve')
    ax.set_ylabel('Maturity')
    ax.set_zlabel('Yield')
    ax.set_xlabel('Term')

    ax.view_init(elev=elev, azim=azim)

    def format_date(x, pos=None):
        return dates.num2date(x).strftime('%Y-%m-%d')

    ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    for tl in ax.w_xaxis.get_ticklabels():
        tl.set_ha('right')
        tl.set_rotation(15)
    fig.colorbar(surf)
    plt.show()
interact(plot_interactive_3d, elev=(0, 90, 5), azim=(0, 360, 5))


