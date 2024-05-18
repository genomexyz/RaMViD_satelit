import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from glob import glob
from mpl_toolkits.basemap import Basemap
import random
import os

from PIL import Image, ImageDraw

#setting
radius = 50
#-0.9189134818610273, 119.90690114318912
target_lat = -0.9189134818610273
target_lon = 119.90690114318912
latbb = -11.0
latba = 6.0
lonbb = 95
lonba = 140.0
total_coordinate = 5000

sample_nc_filename = 'nc/H08_B13_Indonesia_202201020400.nc'


def random_float_with_precision(a, b, precision):
    random_number = random.uniform(a, b)
    format_string = "{:." + str(precision) + "f}"
    random_number_with_precision = format_string.format(random_number)
    return float(random_number_with_precision)

def find_idx(coordinate, mat_coordinate):
    #sanitize start
    if len(mat_coordinate) < 5:
        print('mat coordinate terlalu sedikit')
        return None
    if len(np.shape(mat_coordinate)) > 1:
        print('mat harus 1d')
        return None
    #sanitize end

    #first find is the mat is ascend or descend?
    cor1 = mat_coordinate[0]
    cor2 = mat_coordinate[1]

    if cor2 > cor1:
        for i in range(len(mat_coordinate)):
            if mat_coordinate[i] > coordinate:
                candidate_cor1 = mat_coordinate[i]
                idx_cor1 = i
                if mat_coordinate[i] == 0:
                    return 0
                candidate_cor2 = mat_coordinate[i-1]
                idx_cor2 = i-1
                break
    elif cor2 < cor1:
        for i in range(len(mat_coordinate)):
            if mat_coordinate[i] < coordinate:
                candidate_cor1 = mat_coordinate[i]
                idx_cor1 = i
                if mat_coordinate[i] == 0:
                    return candidate_cor1
                candidate_cor2 = mat_coordinate[i-1]
                idx_cor2 = i-1
                break
    else:
        print('mat coordinate nilainya tidak valid')
        return None

    dif1 = abs(candidate_cor1-coordinate)
    dif2 = abs(candidate_cor2-coordinate)
    if dif2 < dif1:
        return idx_cor2
    else:
        return idx_cor1



#lat_pusat = []
#lon_pusat = []
##generate coordinate random
#for iter_rand in range(total_coordinate):
#    single_lat = random_float_with_precision(latbb, latba, 5)
#    single_lon = random_float_with_precision(lonbb, lonba, 5)
#    lat_pusat.append(single_lat)
#    lon_pusat.append(single_lon)
#lat_pusat = np.array(lat_pusat)
#lon_pusat = np.array(lon_pusat)
#print(lat_pusat)
#print(lon_pusat)

#list_data_used = ['nc/H08_B13_Indonesia_202201020400.nc', 'nc/H08_B13_Indonesia_202201020410.nc', 
#                  'nc/H08_B13_Indonesia_202201020420.nc', 'nc/H08_B13_Indonesia_202201020430.nc',
#                  'nc/H08_B13_Indonesia_202201020440.nc', 'nc/H08_B13_Indonesia_202201020450.nc',
#                  'nc/H08_B13_Indonesia_202201020500.nc', 'nc/H08_B13_Indonesia_202201020510.nc',
#                  'nc/H08_B13_Indonesia_202201020520.nc', 'nc/H08_B13_Indonesia_202201020530.nc']

list_data_used = sorted(glob('nc/*.nc'))

print(list_data_used)

dset_sample = Dataset(sample_nc_filename)
lat = dset_sample['latitude'][:]
lon = dset_sample['longitude'][:]

idx_lat = find_idx(target_lat, lat)
idx_lon = find_idx(target_lon, lon)
lonlow = idx_lon-radius
lonhigh = idx_lon+radius
latlow = idx_lat-radius
lathigh = idx_lat+radius

total_frame_gif = 20
max_val = 60
min_val = -100
cnt_data = 0
for iter_data in range(len(list_data_used)):
    cnt_gif = []
    if iter_data+total_frame_gif > len(list_data_used):
        break
    for iter_file in range(iter_data, iter_data+total_frame_gif):
        single_nc = list_data_used[iter_file]
        try:
            dset_nc = Dataset(single_nc)
        except OSError:
            cnt_gif = []
            break
        data = dset_nc['IR'][0, latlow:lathigh, lonlow:lonhigh]
        data = data - 273.15
        data[data > max_val] = max_val
        data[data < min_val] = min_val

        data = (data - min_val) / (max_val - min_val) * 255
        #reverse color
        data = 255 - data
        data = data.astype(np.uint8)

        cnt_gif.append(data)
        #if len(cnt_gif) >=  total_frame_gif:
    images = []
    # Create a new grayscale image
    for iter_frame in range(total_frame_gif):
        # Create an image from the array
        img = Image.fromarray(cnt_gif[iter_frame], mode='L')
        images.append(img)
    # Save the sequence of images as a GIF
    images[0].save('gif_dset/%s.gif'%(iter_data+1), save_all=True, append_images=images[1:], loop=0, duration=100)
            


exit()
for iter_pusat in range(len(lat_pusat)):
    print('process iter %s'%(iter_pusat+1))
    single_lat = lat_pusat[iter_pusat]
    single_lon = lon_pusat[iter_pusat]
    idx_lat = find_idx(single_lat, lat)
    idx_lon = find_idx(single_lon, lon)
    lonlow = idx_lon-radius
    lonhigh = idx_lon+radius
    latlow = idx_lat-radius
    lathigh = idx_lat+radius

    lat_used = lat[latlow:lathigh]
    lon_used = lon[lonlow:lonhigh]
    lat_used = np.ma.getdata(lat_used)
    lon_used = np.ma.getdata(lon_used)
    dir_save_coordinate = 'all_sampel_nc2/coordinate/%s'%(iter_pusat+1)
    dir_save_mat = 'all_sampel_nc2/mat/%s'%(iter_pusat+1)
    if not os.path.exists(dir_save_coordinate):
        os.makedirs(dir_save_coordinate)
    if not os.path.exists(dir_save_mat):
        os.makedirs(dir_save_mat)
    np.save(dir_save_coordinate+'/lat.npy', lat_used)
    np.save(dir_save_coordinate+'/lon.npy', lon_used)
    for iter_data in range(len(list_data_used)):
        single_nc = list_data_used[iter_data]
        dset_nc = Dataset(single_nc)
        data = dset_nc['IR'][0, latlow:lathigh, lonlow:lonhigh]
        data = np.ma.getdata(data)
        #print(data, np.shape(data))
        np.save(dir_save_mat+'/%s.npy'%(iter_data+1), data)

