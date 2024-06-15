import shutil
import os
import arcpy

storeDIR = r'E:\Grid_Inputs\CCSM4'
elevDIR = r'E:\Grid_Inputs\DEM'
featDIR = r'E:\Ground_Inputs'
dataDIR = r'C:\Users\afullhart\Documents\ArcGIS\Projects\CCSM4\Data'
gdbDIR = r'C:\Users\afullhart\Documents\ArcGIS\Projects\CCSM4\CCSM4.gdb'

arcpy.env.workspace = gdbDIR
arcpy.env.overwriteOutput = True

var_labels = ['MEAN_', 'SDEV_', 'SKEW_', 'MX5P_', 'RATIO_', 'TIMEPK_']
covar_labels = ['accm_1974_2013_', 'tmax_1974_2013_', 'srad_1974_2013_', 'DEM']

extent = [42.995833333333, -120.995833333333, -102.004166666666, 30.004166666666]

map_io_data = []
for label in var_labels:
  for mo in range(1, 13):
    ground = label + str(mo) + '.txt'
    covars = [var + str(mo) + '.tif' for var in covar_labels[:-1]]
    covars.append(covar_labels[-1] + '.tif')
    map_io_data.append([ground, covars])


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
  
  arcpy.management.XYTableToPoint(
    in_table=featA,
    out_feature_class=ground.strip('.txt'),
    x_field="x",
    y_field="y",
    z_field=None,
    coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision'
  )
  
  arcpy.ga.EBKRegressionPrediction(
    in_features=ground.strip('.txt'),
    in_explanatory_rasters=[rasterA, rasterB, rasterC, rasterD],
    dependent_field='data',
    out_ga_layer='EBK Regression Prediction',
    min_cumulative_variance=95,
    overlap_factor=1,
    number_simulations=100,
    semivariogram_model_type='EXPONENTIAL',
    search_neighborhood=arcpy.SearchNeighborhoodStandardCircular(1.1786916595137806, 0, 15, 10, 'ONE_SECTOR')
  )    
  
  outputCoordinateSystem = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
  snapRaster = rasterD
  parallelProcessingFactor = '3'
  extent = '-120.995833333333 30.004166666666 -102.004166666666 42.995833333333 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]' 
  cellSize = rasterD
  mask = os.path.join(dataDIR, 'Study_Area_Shp', 'Study_Area_Shp.shp')
  
  with arcpy.EnvManager(outputCoordinateSystem=outputCoordinateSystem, snapRaster=snapRaster, parallelProcessingFactor=parallelProcessingFactor, cellSize=cellSize, mask=mask):
    arcpy.ga.GALayerToGrid(
      in_geostat_layer='EBK Regression Prediction',
      out_surface_grid=ground.strip('.txt') + '_clip',
      cell_size=0.008333333333,
      points_per_block_horz=1,
      points_per_block_vert=1
    )

  arcpy.management.Delete(ground.strip('.txt'))
  arcpy.management.Rename(ground.strip('.txt') + '_clip', ground.strip('.txt'))

  os.remove(featA)
  os.remove(rasterA)
  os.remove(rasterB)
  os.remove(rasterC)
  os.remove(rasterD)
  




