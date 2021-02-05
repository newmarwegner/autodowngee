from itertools import groupby
import ee
import geemap
import geopandas as gpd
import os
import rasterio
from rasterio.merge import merge
import shutil

# function to initialize gee
def initialize():
    ee.Authenticate()
    ee.Initialize()

    return

# function to open a shapefile
def open_shp(shapefile):
    path = f'{os.getcwd()}/dados/{shapefile}'

    return gpd.read_file(path)

# function to verify if has folder and create if not
def has_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

    return

# create list by attributes of shapefile
def get_class(filter_field):
    polygons = open_shp(shapefile)

    return list(set([v[filter_field] for k,v in polygons.iterrows()]))

# function to get each polygon
def filter_polygon(filter_field, feature_name, polygons):
    filter_polygon = polygons.loc[(polygons[filter_field] == feature_name)]
    xmin, ymin, xmax, ymax = filter_polygon.total_bounds
    box=[[xmin,ymin],[xmin,ymax],[xmax,ymax],[xmax,ymin],[xmin,ymin]]

    return filter_polygon, box

# function to download gee
def download_ndvi(feature_name,box, start_date,end_date):
    has_folder(os.getcwd()+'/output/')
    out_dir = os.getcwd()+'/output/'+ str(feature_name)
    boundary = ee.Geometry.Polygon(box, None, False)
    collection = ee.ImageCollection(path_collection) \
                 .filterDate(start_date,end_date)

    return geemap.ee_export_image_collection(collection,scale=30,crs='EPSG:4326',region=boundary, out_dir=out_dir)

# function to return path of outputs
def output_paths():
    output_paths = []
    for root, directory, files in os.walk(os.getcwd()+'/output'):
        if not root.endswith('/output'):
            dir_path = root+'/'
            for file in files:
                if file.endswith('.tif'):
                    full_path = f"{dir_path}{dir_path.split('/')[-2]}_{file}"

                    output_paths.append(full_path)

    return output_paths

#function to group path rasters
def grouppath_mosaic(paths_to_mosaic):
    func = lambda x: x[-9:]
    temp = sorted(paths_to_mosaic, key=func)

    return [list(paths_to_mosaic) for i, paths_to_mosaic in groupby(temp,func)]

# function to mosaic
def create_mosaic(path_groups):
    has_folder(os.getcwd()+'/merged/')
    for i in path_groups:
        ano = i[0][-8:-4]
        src_files_to_mosaic = []
        out_meta = []
        count = 0
        for file in i:
            full = ''.join([file[:file.rfind('/')+1],file[file.rfind('_')+1:]])
            src = rasterio.open(full)
            src_files_to_mosaic.append(src)
            out_meta = src.meta.copy()

        mosaic, out_trans = merge(src_files_to_mosaic)
        out_meta.update({"driver": "GTiff",
                         "height": mosaic.shape[1],
                         "width": mosaic.shape[2],
                         "transform": out_trans,
                         "crs": "+proj=longlat +datum=WGS84 +no_defs"
                         }
        )
        with rasterio.open(f'{os.getcwd()}/merged/{count}_{ano}.tif',"w",**out_meta) as dest:
            dest.write(mosaic)
        count += 1
    return

# function to remove folders not merged
def remove_not_merged():
    
    return shutil.rmtree(f'{os.getcwd()}/output')

# Run program
if __name__ == '__main__':
    
    start_date='1999-01-01'
    end_date='2001-04-25'
    filter_field = 'id'
    shapefile = 'limite_test.shp'
    path_collection = "LANDSAT/LE7_L1T_ANNUAL_NDVI"
    
    initialize()
    polygons = open_shp(shapefile)
    feature_names = get_class(filter_field)

    for feature_name in feature_names:
        polygon, box = filter_polygon(filter_field, feature_name, polygons)
        download_ndvi(feature_name,box, start_date, end_date)

    list_to_mosaic = output_paths()
    path_groups = grouppath_mosaic(list_to_mosaic)
    create_mosaic(path_groups)
    remove_not_merged()
 




