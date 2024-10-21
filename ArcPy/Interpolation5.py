###############################################################################
'Calculate PWW and PWD from RATIO, MEANP, and ACCM'
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

arcpy.env.workspace = gdbDIR
arcpy.env.overwriteOutput = True

var_labels = ['accm', 'mean', 'ratio']
year_labels = ['1974_2013', '2000_2029', '2010_2039', '2020_2049', '2030_2059', '2040_2069', '2050_2079', '2060_2089', '2070_2099']

extent = [43.0, -121.0, -102.0, 30.0]

ndays = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

map_io_data = []
for mo in range(1, 13):
  for yrlabel in year_labels:
    map_io_data.append([yrlabel, mo])

for io in map_io_data:
  
  print(io)
  yrlabel = io[0]
  mo = io[1]
  
  outputCoordinateSystem = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
  parallelProcessingFactor = '5'
  extent = '-121.0 30.0 -102.0 43.0 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'

  with arcpy.EnvManager(outputCoordinateSystem=outputCoordinateSystem, extent=extent, parallelProcessingFactor=parallelProcessingFactor):

    accm = 'accm_{}_{}'.format(yrlabel, str(mo))
    mean = 'mean_{}_{}'.format(yrlabel, str(mo))
    ratio = 'ratio_1974_2013_{}'.format(str(mo))
    pwd = 'pwd_{}_{}'.format(yrlabel, str(mo))
    
    output_raster = arcpy.sa.RasterCalculator(
      rasters=[accm, mean, ratio],
      input_names=['accm', 'mean', 'ratio'],
      expression='Con(IsNull(accm), accm, 1/((1/(((accm/25.4)/mean)/{})) + ratio - 1))'.format(str(ndays[mo-1]))
    )

    output_raster.save('pwd_{}_{}'.format(yrlabel, str(mo)))

    output_raster = arcpy.sa.RasterCalculator(
      rasters=[accm, pwd, ratio],
      input_names=['accm', 'pwd', 'ratio'],
      expression='Con(IsNull(accm), accm, ratio*pwd)'
    )

    output_raster.save('pww_{}_{}'.format(yrlabel, str(mo)))

