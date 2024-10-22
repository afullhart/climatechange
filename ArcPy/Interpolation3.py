###############################################################################
'Future surfaces based on delta method and smoothed focal point surfaces'
###############################################################################

import shutil
import os
import arcpy
import numpy as np

gcmLabel = 'CCSM4'

storeDIR = r'E:\Grid_Inputs\{}'.format(gcmLabel)
featDIR = r'E:\Ground_Inputs'
dataDIR = r'C:\Users\afullhart\Documents\ArcGIS\Projects\{}\Data'.format(gcmLabel)
gdbDIR = r'C:\Users\afullhart\Documents\ArcGIS\Projects\{}\{}.gdb'.format(gcmLabel, gcmLabel)
storeshpDIR = r'E:\Study_Area_Shp'
maskSHP = os.path.join(dataDIR, 'Study_Area_Shp', 'Study_Area_Shp.shp')
  
if not os.path.exists(maskSHP):
  shutil.copytree(storeshpDIR, os.path.join(dataDIR, 'Study_Area_Shp'))

if not os.path.exists(dataDIR):
  os.makedirs(dataDIR)

arcpy.env.workspace = gdbDIR
arcpy.env.overwriteOutput = True
arcpy.env.randomGenerator = '123 ACM599'

var_labels = ['mean', 'sdev', 'skew']
grid_labels = ['mean', 'sdev', 'skew']
year_labels = ['2000_2029', '2010_2039', '2020_2049', '2030_2059', '2040_2069', '2050_2079', '2060_2089', '2070_2099']
extent = [43.0, -121.0, -102.0, 30.0]

map_io_data = []
for i, label in enumerate(var_labels):
  for yrlabel in year_labels:
    for mo in range(1, 13):
      ground = var_labels[i] + '_1974_2013_' + str(mo)
      grids = [grid_labels[i] + '_1974_2013_' + str(mo) + '.tif', grid_labels[i] + '_' + yrlabel + '_' + str(mo) + '.tif']
      map_io_data.append([ground, grids])

with open(os.path.join(dataDIR, 'FOCAL_RMSE.csv'), 'w') as fo:
  fo.write('map,rmse,pbias,mape\n')
  for io in map_io_data:
    ground = io[0]
    grids = io[1]
    
    rasterBB = os.path.join(storeDIR, grids[0])
    rasterCC = os.path.join(storeDIR, grids[1])

    rasterB = os.path.join(dataDIR, grids[0])
    rasterC = os.path.join(dataDIR, grids[1])
    rasterD = 'DEM'
  
    print(rasterB)
    print(rasterC)
    print(rasterD)
  
    shutil.copyfile(rasterBB, rasterB)
    shutil.copyfile(rasterCC, rasterC)
  
    outputCoordinateSystem='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
    snapRaster=rasterD
    extent='-121.0 30.0 -102.0 43.0 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
    cellSize=rasterD
    
    for raster in [rasterB, rasterC]:
  
      with arcpy.EnvManager(outputCoordinateSystem=outputCoordinateSystem, snapRaster=snapRaster, extent=extent, cellSize=cellSize):
        out_raster = arcpy.sa.FocalStatistics(
          in_raster=raster,
          neighborhood='Circle 7 CELL',
          statistics_type='MEDIAN',
          ignore_nodata='NODATA',
          percentile_value=90
        )
        out_raster.save(raster.split('\\')[-1][:-4] + '_f')


    f_raster_str = raster.split('\\')[-1][:-4] + '_f'
    sqrerr_raster = arcpy.sa.RasterCalculator(
      rasters=[raster, f_raster_str],
      input_names=['gridt1', 'gridt1f'],
      expression='(gridt1 - gridt1f)**2'
    )
  
    sqrerr_raster.save('sqrerr')
    mse_diff = arcpy.management.GetRasterProperties(sqrerr_raster, 'MEAN')
    mse_diff_str = str(mse_diff)
    rmse_diff = (float(mse_diff_str)**0.5)/25.4
    arcpy.management.Delete('sqrerr')


    err_raster = arcpy.sa.RasterCalculator(
      rasters=[raster, f_raster_str],
      input_names=['gridt1', 'gridt1f'],
      expression='(gridt1 - gridt1f)'
    )
    
    err_raster.save('err')
    err_arr = arcpy.RasterToNumPyArray('err')
    obs_arr = arcpy.RasterToNumPyArray(raster)
    sumerr_diff = np.nansum(err_arr)
    sumobs_diff = np.nansum(obs_arr)
    pbias_diff = 100*(sumerr_diff/sumobs_diff)

    relerr_diff = np.absolute(np.divide(err_arr, obs_arr))
    mape_diff = 100*(1/obs_arr[obs_arr > 0].size)*np.nansum(relerr_diff)
    arcpy.management.Delete('err')


    fo.write(f_raster_str + ',' + str(rmse_diff) + ',' + str(pbias_diff) + ',' + str(mape_diff) + '\n')


    if 'skew' not in ground:
      output_raster = arcpy.sa.RasterCalculator(
        rasters=[ground, grids[0].split('\\')[-1][:-4] + '_f', grids[1].split('\\')[-1][:-4] + '_f'],
        input_names=['groundt1', 'gridt1', 'gridt2'],
        expression='(groundt1/(gridt1/25.4))*(gridt2/25.4)'
      )
  
    else:
      output_raster = arcpy.sa.RasterCalculator(
        rasters=[ground, grids[0].split('\\')[-1][:-4] + '_f', grids[1].split('\\')[-1][:-4] + '_f'],
        input_names=['groundt1', 'gridt1', 'gridt2'],
        expression='(groundt1/gridt1)*(gridt2)'
      )
    
    output_raster.save(grids[1].split('\\')[-1][:-4])  
  
    outExtractByMask = arcpy.sa.ExtractByMask(grids[1].split('\\')[-1][:-4], maskSHP, 'INSIDE')
    outExtractByMask.save(grids[1].split('\\')[-1][:-4])
  
    arcpy.management.Delete(rasterB.split('\\')[-1][:-4] + '_f')
    arcpy.management.Delete(rasterC.split('\\')[-1][:-4] + '_f')
    os.remove(rasterB)
    if os.path.exists(rasterC):
      os.remove(rasterC)

