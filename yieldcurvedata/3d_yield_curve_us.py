# %% [markdown]
# # 3-D Plot of the US Treasury yield curve
# 
# - Author: Ian Blaiklock
# - Date: 3/25/2015
# - Note: Based on The Upshot's (NY Times) 3/18/2015 [post](http://www.nytimes.com/interactive/2015/03/19/upshot/3d-yield-curve-economic-growth.html?abt=0002&abg=1) titled 'A 3-D View of a Chart That Predicts The Economic Future: The Yield Curve' by Gregor Aisch and Amanda Cox.
# 
# The US Treasury yield curve represents the relationship between maturity and yields. For more info see http://en.wikipedia.org/wiki/Yield_curve.
# 
# The typical plot of historical yield curves is 2-D where the user has to pick various reference points over time. However, without always knowing how the curve has changed over time selecting those points is often difficult.
# 
# The Upshot used yields on treasuries since 1990 and plotted the yield curve as a time series in 3-D. I thought that the result was the coolest thing and set out to do the same thing using Python.
# 
# I used [Quandl](https://www.quandl.com/data/USTREASURY/YIELD-Treasury-Yield-Curve-Rates) as the link between my script and the Treasury's [data](http://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldAll).
# 
# Some helpful links along the way include:
# 
# - Matplotlib's mplot3d surface plot [tutorial](http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#surface-plots)
# - Matplotlib [dates](http://matplotlib.org/api/dates_api.html)
# - SciPy's numpy array creation routines [reference](http://docs.scipy.org/doc/numpy/reference/routines.array-creation.html)

# %% [markdown]
# ### Preliminaries

# %%
# Python3.9.9
%matplotlib inline
import quandl
import numpy as np
from mpl_toolkits.mplot3d import axes3d

import matplotlib.dates as dates
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

# %% [markdown]
# ### Quandl
# 
# We aren't doing anything super special to get data from Quandl. Once we have the series name, `USTREASURY/YIELD`, it is a simple call using Quandl's `.get` method. 
# 
# Since I was following the mplot3d tutorial I decided to return the data as a numpy `recarray`, which is not the default return format. 
# 
# The `.get` method also makes it really easy to select a specific date range using `trim_start` and `trim_end`. The US Treasury data starts on 1990-01-02.

# %%
# data = quandl.get('USTREASURY/YIELD', returns='numpy', trim_start="2021-01-01")
data = quandl.get('USTREASURY/YIELD', returns='numpy', trim_start="2022-06-01")

# %% [markdown]
# A quick look at the data

# %%
data

# %% [markdown]
# ### Transforming the data
# In order to use matplotlib's `surface_plot` function (*or at least mimic the tutorial*) we need 3 numpy arrays. The `x` array will consist of the dates, the `y` array will consist of maturities and the `z` array will consist of the yields.
# 
# Before we dig in building any arrays we need to convert the header row (strings) received from Quandl into actual floating point numbers.

# %%
# Header row from Quandl
print(data.dtype.names)

# %%
# Conversion
header = []
for name in data.dtype.names[1:]:
    maturity = float(name.split(" ")[0])
    if name.split(" ")[1] == 'Mo':
        maturity = maturity / 12
    header.append(maturity)
print(header)

# %% [markdown]
# My (*probably inefficient*) plan for building the arrays is to convert the `recarray` received from Quandl into lists in order to element-wise manipulation and then convert back into regular numpy arrays.

# %%
# Some empty lists
x_data = []; y_data = []; z_data = []

# %%
# Convert dates from datetime to numeric
for dt in data.Date:
    dt_num = dates.date2num(dt)
    x_data.append([dt_num for i in range(len(data.dtype.names)-1)])
print('x_data: ', x_data[1:5])

# %% [markdown]
# Each row of our `recarray` from Quandl is a tuple that consists of the date and then entries for each maturity. Our `z` array, which are the yields, needs to be extracted from those tuples.

# %%
# Extract yields from data
for row in data:
    y_data.append(header)
    z_data.append(list(row.tolist()[1:]))
print('y_data: ', y_data[1:10])
print('z_data: ', z_data[1:10])

# %% [markdown]
# ### Build numpy arrays

# %%
x = np.array(x_data, dtype='f'); y = np.array(y_data, dtype='f'); z = np.array(z_data, dtype='f')

# %%
print('x:', x)
print('y: ', y)
print('z: ', z)

# %% [markdown]
# ### Plot the surface plot
# 
# The `format_date` function and method for rotating the x tick labels was modified from this [SO question](http://stackoverflow.com/questions/2195983/matplotlib-formatting-dates-on-the-x-axis-in-a-3d-bar-graph)
# 
# If you want to see a list of available colormaps use `print plt.colormaps()` or visit http://mpastell.com/2013/05/02/matplotlib_colormaps/.
# 
# In order for the colormap to scale the colors correctly (because of the presence of `NaN`s) set `vmin` and `vmax` to their respective min and max from the `z`, yield, array.

# %%
print(plt.colormaps())

# %%
# 左が古い、右が最新
# fig = plt.figure(figsize=(15, 10))
fig = plt.figure(figsize=(30, 20))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=50, cstride=1, cmap='inferno', vmin=np.nanmin(z), vmax=np.nanmax(z))
ax.set_title('US Treasury Yield Curve')
ax.set_ylabel('Maturity')
ax.set_zlabel('Yield')
ax.set_xlabel('Term')
#ax.view_init(elev=230, azim=110)
# SO question
def format_date(x, pos=None):
     return dates.num2date(x).strftime('%Y-%m-%d')

ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
for tl in ax.w_xaxis.get_ticklabels():
    tl.set_ha('right')
    tl.set_rotation(15)
fig.colorbar(surf)
plt.show()

# %%
# 左が古い、右が最新
# fig = plt.figure(figsize=(15, 10))
fig = plt.figure(figsize=(30, 20))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=50, cstride=1, cmap='inferno', vmin=np.nanmin(z), vmax=np.nanmax(z))
ax.set_title('US Treasury Yield Curve')
ax.set_ylabel('Maturity')
ax.set_zlabel('Yield')
ax.set_xlabel('Term')
ax.view_init(elev=10 ,azim=300)
# SO question
def format_date(x, pos=None):
     return dates.num2date(x).strftime('%Y-%m-%d')

ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
for tl in ax.w_xaxis.get_ticklabels():
    tl.set_ha('right')
    tl.set_rotation(15)
fig.colorbar(surf)
plt.show()

# %%
# 左が古い、右が最新
# fig = plt.figure(figsize=(15, 10))
fig = plt.figure(figsize=(30, 20))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=50, cstride=1, cmap='inferno', vmin=np.nanmin(z), vmax=np.nanmax(z))
ax.set_title('US Treasury Yield Curve')
ax.set_ylabel('Maturity')
ax.set_zlabel('Yield')
ax.set_xlabel('Term')
ax.view_init(elev=50 ,azim=70)
# SO question
def format_date(x, pos=None):
     return dates.num2date(x).strftime('%Y-%m-%d')

ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
for tl in ax.w_xaxis.get_ticklabels():
    tl.set_ha('right')
    tl.set_rotation(15)
fig.colorbar(surf)
plt.show()

# %%
# 左が古い、右が最新
# fig = plt.figure(figsize=(15, 10))
fig = plt.figure(figsize=(30, 20))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=50, cstride=1, cmap='inferno', vmin=np.nanmin(z), vmax=np.nanmax(z))
ax.set_title('US Treasury Yield Curve')
ax.set_ylabel('Maturity')
ax.set_zlabel('Yield')
ax.set_xlabel('Term')
# elev y , azim x
ax.view_init(elev=10,azim=270 )
#ax.view_init(elev=230, azim=110)
# SO question
def format_date(x, pos=None):
     return dates.num2date(x).strftime('%Y-%m-%d')

ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
for tl in ax.w_xaxis.get_ticklabels():
    tl.set_ha('right')
    tl.set_rotation(15)
fig.colorbar(surf)
plt.show()

# %%
# 手前が古い、奥が最新
# fig = plt.figure(figsize=(15, 10))
fig = plt.figure(figsize=(30, 20))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=50, cstride=1, cmap='inferno', vmin=np.nanmin(z), vmax=np.nanmax(z))
ax.set_title('US Treasury Yield Curve')
ax.set_ylabel('Maturity')
ax.set_zlabel('Yield')
ax.set_xlabel('Term')
# elev y , azim x
ax.view_init(elev=10,azim=180 )
#ax.view_init(elev=230, azim=110)
# SO question
def format_date(x, pos=None):
     return dates.num2date(x).strftime('%Y-%m-%d')

ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
for tl in ax.w_xaxis.get_ticklabels():
    tl.set_ha('right')
    tl.set_rotation(15)
fig.colorbar(surf)
plt.show()

# %%
# 手間が最新、奥が古い
# fig = plt.figure(figsize=(15, 10))
fig = plt.figure(figsize=(30, 20))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=50, cstride=1, cmap='inferno', vmin=np.nanmin(z), vmax=np.nanmax(z))
ax.set_title('US Treasury Yield Curve')
ax.set_ylabel('Maturity')
ax.set_zlabel('Yield')
ax.set_xlabel('Term')
# elev y , azim x
ax.view_init(elev=10,azim=360 )
#ax.view_init(elev=230, azim=110)
# SO question
def format_date(x, pos=None):
     return dates.num2date(x).strftime('%Y-%m-%d')

ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
for tl in ax.w_xaxis.get_ticklabels():
    tl.set_ha('right')
    tl.set_rotation(15)
fig.colorbar(surf)
plt.show()

# %%



