###############################################################################
'Adds auxiliary rasters to gdb'
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

arcpy.env.workspace = dataDIR
arcpy.env.overwriteOutput = True


var_labels = ['accm', 'tmax', 'tmin', 'txsd', 'tnsd', 'tdew', 'srad', 'srsd']
year_labels = ['_1974_2013_', '_2000_2029_', '_2010_2039_', '_2020_2049_', '_2030_2059_', '_2040_2069_', '_2050_2079_', '_2060_2089_', '_2070_2099_']

extent = [43.0, -121.0, -102.0, 30.0]

map_io_data = []
for mo in range(1, 13):
  for yrlabel in year_labels:
      for varlabel in var_labels:
        grid = varlabel + yrlabel + str(mo) + '.tif'
        map_io_data.append(grid)

for grid in map_io_data:
  
  print(grid)
  
  rasterAA = os.path.join(storeDIR, grid)
  rasterA = os.path.join(dataDIR, grid)
  shutil.copyfile(rasterAA, rasterA)
  
  arcpy.conversion.RasterToGeodatabase(
    Input_Rasters=grid,
    Output_Geodatabase=gdbDIR
    )

  outExtractByMask = arcpy.sa.ExtractByMask(os.path.join(gdbDIR, grid[:-4]), maskSHP, 'INSIDE')
  outExtractByMask.save(os.path.join(gdbDIR, grid[:-4]))

  os.remove(rasterA)

