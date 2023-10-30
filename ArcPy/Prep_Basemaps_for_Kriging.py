import shutil

mapFolder = r'C:\Users\afullhart\Desktop\ClimateChange\Basemaps'
projectFolder = r'C:\Users\afullhart\Documents\ArcGIS\Projects\MyProject'
grndTable = 'MEANP_7.txt'
prcpMap = 'prcp_1974_2013_7.tif'
tempMap = 'tmax_1974_2013_7.tif'
evapMap = 'pet_1974_2013.tif'
elevMap = 'AvgElev3DEP.tif'
gdbName = 'MyProject.gdb'

shutil.copyfile(mapFolder + '\\CLIGEN Network XYZ\\MEANP\\' + grndTable, projectFolder + '\\' + grndTable)
shutil.copyfile(mapFolder + '\\prcp_1974_2013\\' + prcpMap, projectFolder + '\\' + prcpMap)
shutil.copyfile(mapFolder + '\\tmax_1974_2013\\' + tempMap, projectFolder + '\\' + tempMap)
shutil.copyfile(mapFolder + '\\' + evapMap, projectFolder + '\\' + evapMap)
shutil.copyfile(mapFolder + '\\' + elevMap, projectFolder + '\\' + elevMap)



import arcpy
arcpy.env.workspace = projectFolder + '\\' + gdbName
arcpy.env.overwriteOutput = True

in_table = projectFolder + '\\' + grndTable,
out_feature_class = grndTable.strip('.txt'),
x_field = 'x',
y_field = 'y',
z_field = 'data',
coordinate_system = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],VERTCS["WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision'

# arcpy.management.XYTableToPoint(in_table=in_table,
#                                 out_feature_class=out_feature_class,
#                                 x_field=x_field,
#                                 y_field=y_field,
#                                 z_field=z_field,
#                                 coordinate_system=coordinate_system)

# arcpy.management.XYTableToPoint(
#     in_table=r"C:\Users\afullhart\Documents\ArcGIS\Projects\MyProject\MEANP_1.txt",
#     out_feature_class=r"C:\Users\afullhart\Documents\ArcGIS\Projects\MyProject\MyProject.gdb\MEANP_1_XYTableToPoint",
#     x_field="x",
#     y_field="y",
#     z_field="data",
#     coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],VERTCS["WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PARAMETER["Vertical_Shift",0.0],PARAMETER["Direction",1.0],UNIT["Meter",1.0]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')

def repeat_workflow_fn(lyrMap):

    Input_Rasters = projectFolder + '\\' + lyrMap
    Output_Geodatabase = projectFolder + '\\' + gdbName
    Configuration_Keyword = 'MAX_FILE_SIZE_4GB'
    arcpy.conversion.RasterToGeodatabase(
        Input_Rasters=Input_Rasters, 
        Output_Geodatabase=Output_Geodatabase, 
        Configuration_Keyword=Configuration_Keyword)
        
    rasters = [lyrMap]
    input_names = ['x']
    expression ='Int(x*10000)'
    output_raster = arcpy.sa.RasterCalculator(
        rasters=rasters,
        input_names=input_names,
        expression=expression)    
    
    output_raster.save(projectFolder + '\\' + lyrMap.strip('.tif') + '_INT' + '.tif')
    
    in_raster = projectFolder + '\\' + lyrMap.strip('.tif') + '_INT' + '.tif'
    out_rasterlayer = prcpMap.strip('.tif') + '_INT'
    arcpy.MakeRasterLayer_management(
        in_raster=in_raster,
        out_rasterlayer=out_rasterlayer)
    
    in_raster = prcpMap.strip('.tif') + '_INT'
    out_point_features = projectFolder + '\\' + gdbName + '\\' + lyrMap.strip('.tif') + '_INT'
    raster_field = 'Value'
    
    arcpy.conversion.RasterToPoint(
        in_raster=in_raster,
        out_point_features=out_point_features,
        raster_field=raster_field)
    
    return 0



out = repeat_workflow_fn(prcpMap)
out = repeat_workflow_fn(tempMap)    
out = repeat_workflow_fn(evapMap)    
out = repeat_workflow_fn(elevMap)    


