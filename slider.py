import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
# %matplotlib inline
import pysal as ps
from pysal.contrib.viz import mapping as maps
import matplotlib.pyplot as plt
import geopandas as gpd
from pandas import DataFrame
from geopandas import GeoDataFrame
import os, time, glob

fp = "C:\zoovision\data\states\states2.shp"
rg1 = gpd.read_file(fp)
rg1 = rg1.to_crs(epsg=2163)
fig, ax = plt.subplots(1, figsize=(15
                                   , 10))
hr10 = ps.Quantiles(rg1.POP10_SQMI, k=10)
# title = "Select parameters and press query to view surveillance summary"
# ax.set_title(title, y=1.08, fontsize=30)
ax.set_axis_off()

rg1.plot(ax=ax)
# rg1.assign(cl=hr10.yb).plot(column='cl', categorical=True, \
#                  linewidth=0.5, ax=ax,
#                  k = 10, cmap='BuGn', edgecolor='black')

if not os.path.isdir('static'):
    os.mkdir('static')
else:
    # Remove old plot files
    for filename in glob.glob(os.path.join('static', '*.png')):
        os.remove(filename)
# Use time in filename in order make a unique filename that the browser has not chached
plotfile = os.path.join('static', str(time.time()) + '.png')
# plt.savefig(plotfile)
# define demnsions of slider bar
axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

# mapslider= plt.axes
samp = Slider(axfreq, 'Week', 1, 40, valinit=40)


def update(val):
    fig.canvas.draw_idle()


samp.on_changed(update)

plt.show()
