import imageio

import datetime
def date_range(start_dt, end_dt = None):
    start_dt = datetime.datetime.strptime(start_dt, "%Y%m%d")
    if end_dt: end_dt = datetime.datetime.strptime(end_dt, "%Y%m%d")
    while start_dt <= end_dt:
        yield start_dt.strftime("%Y%m%d")
        start_dt += datetime.timedelta(days=1)

filenames = []

for i in date_range('19970818', '20210228'):
    filenames.append('figs/AQI_heat_only/' + str(i) + '.png')


with imageio.get_writer('figs/gifs/Washington_AQI_heatmap.gif', mode='I', duration=0.33) as writer:
    for filename in filenames:
        print(filename)
        image = imageio.imread(filename)
        writer.append_data(image)

print('done')