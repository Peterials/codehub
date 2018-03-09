import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap 
from matplotlib.patches import Polygon
from main import models
def plot(data, filename):
	fig = plt.figure()
	ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
	bmap = Basemap(
			projection='merc', llcrnrlon=117, llcrnrlat=31,
			urcrnrlon=122, urcrnrlat=35, lat_0=29, lon_0=120, resolution='h', area_thresh=1000.0)
	shp_info = bmap.readshapefile('CHN_adm_shp/CHN_adm3','states',drawbounds=False)

	for info, shp in zip(bmap.states_info, bmap.states):
		proid = info['NAME_1']
		if proid == 'Jiangsu':
			poly = Polygon(shp,facecolor='w',edgecolor='b', lw=0.2)
			ax1.add_patch(poly)
	for item in data:
		x, y = bmap(item.longitude, item.latitude)
		bmap.plot(x, y, 'ro', markersize=1)
		
	#bmap.drawcoastlines(color='#78D888')
	bmap.drawcountries(color='#78D2F9')
	bmap.drawmapboundary() 
	bmap.drawparallels(np.arange(29,36,2),labels=[1,0,0,0])
	bmap.drawmeridians(np.arange(116,124,2),labels=[0,0,0,1])
	plt.title('Jiangsu Province')
	plt.savefig(filename + '.png', dpi=100, bbox_inches='tight')
	plt.clf()
	plt.close()
data = models.DistinctPoisSuzhou.objects.all()[:200]
filename = "fig_1"
plot(data, filename)