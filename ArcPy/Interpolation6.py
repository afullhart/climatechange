####
'Makes multi-band rasters.'
'!!!!Save copy of gdb with single-band rasters before running!!!!'
####

import arcpy
import os

gdbDIR = r'C:\Users\afullhart\Documents\ArcGIS\Projects\CCSM4\CCSM4.gdb'

arcpy.env.workspace = gdbDIR

var_labels = ['accm', 'mean', 'sdev', 'skew', 'mx5p', 'pwd', 'pww', 'tmax', 'tmin', 'txsd', 'tnsd', 'tdew', 'srad', 'srsd']
year_labels = ['1974_2013', '2000_2029', '2010_2039', '2020_2049', '2030_2059', '2040_2069', '2050_2079', '2060_2089', '2070_2099']
historical_var_labels = ['ratio', 'timepk']

for varlb in var_labels:
  for yrlb in year_labels:
    rasters = []
    for mo in range(1, 13):
      raster_name = '{}_{}_{}'.format(varlb, yrlb, str(mo))
      rasters.append(raster_name)
      
    arcpy.management.CompositeBands(rasters, '{}_{}'.format(varlb, yrlb))      
    for raster in rasters:
      arcpy.management.Delete(raster)

for varlb in historical_var_labels:
  rasters = []
  for mo in range(1, 13):
    raster_name = '{}_1974_2013_{}'.format(varlb, str(mo))
    rasters.append(raster_name)
    
  arcpy.management.CompositeBands(rasters, '{}_1974_2013'.format(varlb))      
  for raster in rasters:
    arcpy.management.Delete(raster)
    



