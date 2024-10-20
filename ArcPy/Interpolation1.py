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
year_labels = ['1974_2013', '2000_2029', '2010_2039', '2020_2049', '2030_2059', '2040_2069', '2050_2079', '2060_2089', '2070_2099']

extent = [43.0, -121.0, -102.0, 30.0]

map_io_data = []
for mo in range(1, 13):
  for yrlabel in year_labels:
      for varlabel in var_labels:
        grid = varlabel + '_' + yrlabel + '_' + str(mo) + '.tif'
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


