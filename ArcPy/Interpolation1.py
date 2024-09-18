###############################################################################
'Historical Kriging Interpolation'
###############################################################################

import shutil
import os
import arcpy
import pandas as pd
import numpy as np

gcmLabel = 'CCSM4'
storeDIR = r'E:\Grid_Inputs\{}'.format(gcmLabel)
elevDIR = r'E:\Grid_Inputs\DEM'
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


var_labels = ['MEAN_', 'SDEV_', 'SKEW_', 'MX5P_', 'RATIO_', 'TIMEPK_']
covar_labels = ['accm_1974_2013_', 'tmax_1974_2013_', 'srad_1974_2013_', 'DEM']

extent = [43.0, -121.0, -102.0, 30.0]

map_io_data = []
for label in var_labels:
  for mo in range(1, 13):
    ground = label + str(mo) + '.txt'
    covars = [var + str(mo) + '.tif' for var in covar_labels[:-1]]
    covars.append(covar_labels[-1] + '.tif')
    map_io_data.append([ground, covars])

with open(os.path.join(dataDIR, 'EBK_CV.csv'), 'w') as fo:
  fo.write('map,rmse,pbias,mape\n')
  for io in map_io_data:  
    
    ground = io[0]
    covars = io[1]
      
    print(ground)
    print(covars)
    
    featAA = os.path.join(featDIR, ground)
    rasterAA = os.path.join(storeDIR, covars[0])
    rasterBB = os.path.join(storeDIR, covars[1])
    rasterCC = os.path.join(storeDIR, covars[2])
    rasterDD = os.path.join(elevDIR, covars[3])
    
    featA = os.path.join(dataDIR, ground)
    rasterA = os.path.join(dataDIR, covars[0])
    rasterB = os.path.join(dataDIR, covars[1])
    rasterC = os.path.join(dataDIR, covars[2])
    rasterD = os.path.join(dataDIR, covars[3])
    
    shutil.copyfile(featAA, featA)
    shutil.copyfile(rasterAA, rasterA)
    shutil.copyfile(rasterBB, rasterB)
    shutil.copyfile(rasterCC, rasterC)
    shutil.copyfile(rasterDD, rasterD)
  
    outputCoordinateSystem = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
    snapRaster = rasterD
    parallelProcessingFactor = '4'
    extent = '-121.0 30.0 -102.0 43.0 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
    cellSize = rasterD
  
    if ground == 'TIMEPK_12.txt':
      with arcpy.EnvManager(outputCoordinateSystem=outputCoordinateSystem, extent=extent, snapRaster=snapRaster, parallelProcessingFactor=parallelProcessingFactor, cellSize=cellSize):
        output_raster = arcpy.sa.RasterCalculator(
          rasters=['TIMEPK_11'],
          input_names=['rasterClp'],
          expression='Con(IsNull(rasterClp), rasterClp, rasterClp/rasterClp)'
        )
        output_raster.save(ground[:-4])
        fo.write(ground[:-4] + ',' + str(0.0) + ',' + str(0.0) + ',' + str(0.0) + '\n')
      break
  
    arcpy.management.XYTableToPoint(
      in_table=featA,
      out_feature_class=ground[:-4] + '_pts',
      x_field="x",
      y_field="y",
      z_field=None,
      coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision'
    )
  
    with arcpy.EnvManager(outputCoordinateSystem=outputCoordinateSystem, extent=extent, snapRaster=snapRaster, parallelProcessingFactor=parallelProcessingFactor, cellSize=cellSize):
      arcpy.ga.EBKRegressionPrediction(
        in_features=ground[:-4] + '_pts',
        in_explanatory_rasters=[rasterA, rasterB, rasterC, rasterD],
        dependent_field='data',
        out_ga_layer='EBK Regression Prediction',
        min_cumulative_variance=95,
        overlap_factor=1,
        number_simulations=30,
        semivariogram_model_type='EXPONENTIAL',
        search_neighborhood=arcpy.SearchNeighborhoodStandardCircular(1.1786916595137806, 0, 15, 10, 'ONE_SECTOR')
      )    
  
    arcpy.ga.CrossValidation(
      in_geostat_layer = 'EBK Regression Prediction',
      out_point_feature_class = 'EBKfeatures'
    )
    
    arcpy.conversion.ExportTable(
      in_table='EBKfeatures', 
      out_table=os.path.join(dataDIR, 'EBKfeatures_ExportTable.csv'), 
    )
    
    df = pd.read_csv(os.path.join(dataDIR, 'EBKfeatures_ExportTable.csv'))
    rmse_diff = np.sqrt(np.mean((df['Predicted']-df['Measured'])**2)) 
    pbias_diff = 100*(np.sum(df['Measured'] - df['Predicted'])/np.sum(df['Measured']))
    mape_diff = 100*(1/df['Measured'].loc[df['Measured'] != 0.0].size)*(np.nansum(np.absolute((df['Measured'] - df['Predicted'])/(df['Measured'].replace(0.0, np.nan)))))            
    fo.write(ground[:-4] + ',' + str(rmse_diff) + ',' + str(pbias_diff) + ',' + str(mape_diff) + '\n')
  
    with arcpy.EnvManager(outputCoordinateSystem=outputCoordinateSystem, extent=extent, snapRaster=snapRaster, parallelProcessingFactor=parallelProcessingFactor, cellSize=cellSize):
      arcpy.ga.GALayerToGrid(
        in_geostat_layer='EBK Regression Prediction',
        out_surface_grid=ground[:-4],
        cell_size=0.008333333333,
        points_per_block_horz=1,
        points_per_block_vert=1
      )
  
    outExtractByMask = arcpy.sa.ExtractByMask(ground[:-4], maskSHP, 'INSIDE')
    outExtractByMask.save(ground[:-4])
  
    arcpy.management.Delete(ground.strip('.txt') + '_pts')
    arcpy.management.Delete('EBKfeatures')
    arcpy.management.Delete(os.path.join(dataDIR, 'EBKfeatures_ExportTable.csv'))
    os.remove(featA)
    os.remove(rasterA)
    os.remove(rasterB)
    os.remove(rasterC)
    os.remove(rasterD)

  
arcpy.management.Delete(ground.strip('.txt') + '_pts')
arcpy.management.Delete('EBKfeatures')
arcpy.management.Delete(os.path.join(dataDIR, 'EBKfeatures_ExportTable.csv'))
os.remove(featA)
os.remove(rasterA)
os.remove(rasterB)
os.remove(rasterC)
os.remove(rasterD)
  
