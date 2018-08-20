import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

arr = np.random.randn(800, 800)
heatmap, xedges, yedges = np.histogram2d(arr[0], arr[1], bins=(30, 30))
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

fig = plt.figure(figsize=(9, 9))
plt.title('Rainbow Heatmap')
plt.ylabel('y')
plt.xlabel('x')
im = plt.imshow(heatmap, extent=extent, origin='lower')
fig.colorbar(im)
plt.savefig('rainbow.png')


import cmaputil as cmu
import cmaputil.cvdutil as cvu
import scipy
# Input colormap name
cmap = 'viridis'

# Optimize
rgb1, jab1 = cmu.get_rgb_jab(cmap) # Original colormap
rgb2, jab2 = cmu.get_rgb_jab(cvu.get_cvd(rgb1)) # CVD colormap
jab3 = cmu.make_linear(jab2) # Uniformize hue (a' vs. b')
#print(jab3)
_, jab4 = cmu.correct_J(jab3) # Linearize J'

# Convert back to sRGB
rgb4 = cmu.convert(jab4, cmu.CSPACE2, cmu.CSPACE1)
rgb4 = np.clip(rgb4, 0, 1)

# Resimulate CVD in case corrections took the map outside CVD-safe space
rgb4 = cvu.get_cvd(rgb4)


# Resimulate CVD in case corrections took the map outside CVD-safe space
rgb4 = cvu.get_cvd(rgb4)

colors = []
for j in range(len(rgb4[0])):
    colors.append( (rgb4[0][j],
                 rgb4[1][j],
                 rgb4[2][j]) )
                 


# Convert to matplotlib colormap
cmap = mpl.colors.LinearSegmentedColormap.from_list("", colors)

plt.clf()
fig =  plt.figure(figsize=(9, 9))
plt.title('Cividis Heatmap')
plt.ylabel('y')
plt.xlabel('x')
im = plt.imshow(heatmap, extent=extent, cmap=cmap, origin='lower')
fig.colorbar(im)
plt.savefig('Cividis Heatmap')


plt.clf
fig =  plt.figure(figsize=(9, 9))
plt.subplot(1, 2, 1)
plt.title('Rainbow Heatmap')
plt.ylabel('y')
plt.xlabel('x')
plt.imshow(heatmap, extent=extent, origin='lower')
plt.subplot(1, 2, 2)
plt.title('Cividis Heatmap')
plt.ylabel('y')
plt.xlabel('x')
plt.imshow(heatmap, extent=extent, cmap=cmap, origin='lower')
plt.savefig('side_by_side.png')