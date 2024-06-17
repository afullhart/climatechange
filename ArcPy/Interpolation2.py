import shutil
import os
import arcpy


storeDIR = r'E:\Grid_Inputs\CCSM4'
elevDIR = r'E:\Grid_Inputs\DEM'
featDIR = r'E:\Ground_Inputs'
dataDIR = r'C:\Users\afullhart\Documents\ArcGIS\Projects\CCSM4\Data'
gdbDIR = r'C:\Users\afullhart\Documents\ArcGIS\Projects\CCSM4\CCSM4.gdb'
maskSHP = os.path.join(dataDIR, 'Study_Area_Shp', 'Study_Area_Shp.shp')
  
arcpy.env.workspace = gdbDIR
arcpy.env.overwriteOutput = True

var_labels = ['MEAN_', 'SDEV_', 'SKEW_']
grid_labels = ['mean_', 'sdev_', 'skew_']
year_labels = ['2000_2029', '2010_2039', '2020_2049', '2030_2059', '2040_2069', '2050_2079', '2060_2089', '2070_2099']

extent = [42.995833333333, -120.995833333333, -102.004166666666, 30.004166666666]


map_io_data = []
for i, label in enumerate(var_labels):
  for yrlabel in year_labels:
    for mo in range(1, 13):
      ground = var_labels[i] + str(mo)
      grids = [grid_labels[i] + '1974_2013_' + str(mo) + '.tif', grid_labels[i] + yrlabel + '_' + str(mo) + '.tif']
      map_io_data.append([ground, grids])
   

for io in map_io_data:
  ground = io[0]
  grids = io[1]
  
  rasterBB = os.path.join(storeDIR, grids[0])
  rasterCC = os.path.join(storeDIR, grids[1])
  rasterDD = os.path.join(elevDIR, 'DEM.tif')
  
  rasterB = os.path.join(dataDIR, grids[0])
  rasterC = os.path.join(dataDIR, grids[1])
  rasterD = os.path.join(dataDIR, 'DEM.tif')

  print(rasterB)
  print(rasterC)
  print(rasterD)

  shutil.copyfile(rasterBB, rasterB)
  shutil.copyfile(rasterCC, rasterC)
  shutil.copyfile(rasterDD, rasterD)

  for raster in [rasterB, rasterC]:
    
    outputCoordinateSystem='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
    snapRaster=rasterD
    extent='-120.995833333333 30.004166666666 -102.004166666666 42.995833333333 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
    cellSize=0.008333333333
    with arcpy.EnvManager(outputCoordinateSystem=outputCoordinateSystem, snapRaster=snapRaster, extent=extent, cellSize=cellSize):
      out_raster = arcpy.sa.FocalStatistics(
        in_raster=raster,
        neighborhood='Circle 7 CELL',
        statistics_type='MEDIAN',
        ignore_nodata='NODATA',
        percentile_value=90
      )
      out_raster.save(raster.split('\\')[-1].strip('.tif') + '_f')



  if 'SKEW' not in ground:
    output_raster = arcpy.sa.RasterCalculator(
      rasters=[ground, grids[0].split('\\')[-1].strip('.tif') + '_f', grids[1].split('\\')[-1].strip('.tif') + '_f'],
      input_names=['groundt1', 'gridt1', 'gridt2'],
      expression="(groundt1/(gridt1/25.4))*(gridt2/25.4)"
    )

  else:
    output_raster = arcpy.sa.RasterCalculator(
      rasters=[ground, grids[0].split('\\')[-1].strip('.tif') + '_f', grids[1].split('\\')[-1].strip('.tif') + '_f'],
      input_names=['groundt1', 'gridt1', 'gridt2'],
      expression="(groundt1/gridt1)*(gridt2)"
    )
  
  output_raster.save(grids[1].split('\\')[-1].strip('.tif') + '_adj')  

  outExtractByMask = arcpy.sa.ExtractByMask(grids[1].split('\\')[-1].strip('.tif') + '_adj', maskSHP, 'INSIDE')
  outExtractByMask.save(grids[1].split('\\')[-1].strip('.tif') + '_adj')
   
  os.remove(rasterB)
  os.remove(rasterC)
  os.remove(rasterD)
  arcpy.management.Delete(rasterB.split('\\')[-1].strip('.tif') + '_f')
  arcpy.management.Delete(rasterC.split('\\')[-1].strip('.tif') + '_f')

    


