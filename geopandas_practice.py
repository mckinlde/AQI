import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import datetime

def date_range(start_dt, end_dt = None):
    start_dt = datetime.datetime.strptime(start_dt, "%Y%m%d")
    if end_dt: end_dt = datetime.datetime.strptime(end_dt, "%Y%m%d")
    while start_dt <= end_dt:
        yield start_dt.strftime("%Y%m%d")
        start_dt += datetime.timedelta(days=1)

## Defning a colormap so that our scale matches the WA State AQI (normally not this involved)
viridis = cm.get_cmap('viridis', 350)
newcolors = viridis(np.linspace(0, 1, 350))
green = np.array([30 / 350, 130 / 350, 76 / 350, 1])
yellow = np.array([244 / 350, 208 / 350, 63 / 350, 1])
orange = np.array([248 / 350, 148 / 350, 6 / 350, 1])
red = np.array([207 / 350, 0 / 350, 15 / 350, 1])
purple = np.array([102 / 350, 51 / 350, 153 / 350, 1])
darkRed = np.array([150 / 350, 40 / 350, 27 / 350, 1])
newcolors[:50, :] = green
newcolors[50:100, :] = yellow
newcolors[100:150, :] = orange
newcolors[150:200, :] = red
newcolors[200:300, :] = purple
newcolors[300:, :] = darkRed
newcmp = ListedColormap(newcolors)

## Reading data
aqi = gpd.read_file('aqi_temp_data/AQI_by_County_1970_2021.csv')

## TODO: this refers to the file that geopandas uses to generate maps; .shp is a dedicated format
country = gpd.read_file('data/county.shp')
#print(aqi.head())

for i in date_range('19970818', '20210228'):
    print(i)
    dancinginseptember = aqi[aqi['Date'] == str(i)]
    #dancinginseptember = aqi[aqi['Date'] == '20090901']
    dancinginseptember = dancinginseptember.rename(columns={"County.Name": "COUNTY"})
    #print(dancinginseptember.head())

    washington = country[country['STATE'] == 'Washington']
    #print(washington.head())


    graphygraph = washington.merge(dancinginseptember, on='COUNTY', how='outer')
    graphygraph['AQI'] = pd.to_numeric(graphygraph['AQI'])
    graphygraph['COUNTY'].append(washington['COUNTY'])
    #print(graphygraph.head())
    graphygraph = gpd.GeoDataFrame(graphygraph)
    graphygraph = graphygraph.rename(columns={"geometry": "geometry_x"}).set_geometry("geometry_x")

    fig, ax = plt.subplots(1, 1)
    plt.tick_params(left=False, right=False, labelleft=False,
                    labelbottom=False, bottom=False)
    #0-3 yyyy 4-5 mm 6-7 dd
    plt.title("Air Quality Index by County: "+str(i)[4:6]+"/"+str(i)[6:]+"/"+str(i)[0:4])
    graphygraph.plot(column='AQI',
                     cmap=newcmp,
                     ax=ax,
                     legend=True,
                     vmin=0,
                     vmax=350,
                     legend_kwds={'label': "AQI",
                                  'orientation': 'horizontal'},
                     missing_kwds = {"color": "lightgrey"}
                     )
    plt.savefig('figs/AQI_heat_only/'+str(i)+'.png')
    plt.close()
    print('saved')

    #ValueError: Colormap 0rRd is not recognized. Possible values are: Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, winter, winter_r


https://seattleu.zoom.us/j/93091231443