###############################################################################
'MX5P surfaces from gradient boosting'
###############################################################################

import shutil
import os
import arcpy
import pandas as pd
import numpy as np

storeDIR = r'E:\Grid_Inputs\CCSM4'
elevDIR = r'E:\Grid_Inputs\DEM'
featDIR = r'E:\Ground_Inputs'
dataDIR = r'C:\Users\afullhart\Documents\ArcGIS\Projects\CCSM4\Data'
gdbDIR = r'C:\Users\afullhart\Documents\ArcGIS\Projects\CCSM4\CCSM4.gdb'
storeshpDIR = r'E:\Study_Area_Shp'
maskSHP = os.path.join(dataDIR, 'Study_Area_Shp', 'Study_Area_Shp.shp')
  

if not os.path.exists(maskSHP):
  shutil.copytree(storeshpDIR, os.path.join(dataDIR, 'Study_Area_Shp'))


arcpy.env.workspace = dataDIR
arcpy.env.overwriteOutput = True
arcpy.env.randomGenerator = '123 ACM599'

var_labels = ['MX5P']
covar_labels = ['accm', 'tmax', 'srad']
year_labels = ['_1974_2013_', '_2000_2029_', '_2010_2039_', '_2020_2049_', '_2030_2059_', '_2040_2069_', '_2050_2079_', '_2060_2089_', '_2070_2099_']

extent = [43.0, -121.0, -102.0, 30.0]

map_io_data = []
for mo in range(1, 13):
  ground = 'MX5P_{}'.format(mo) + '.txt'
  for yrlabel in year_labels:
    grids = [covar + yrlabel + str(mo) + '.tif' for covar in covar_labels]
    grids.append('DEM.tif')
    map_io_data.append([ground, grids])

with open(os.path.join(dataDIR, 'GB_CV.csv'), 'w') as fo:
  fo.write('map,rmse,pbias\n')
  for i, io in enumerate(map_io_data):
    
    print('\nITERATION INDEX\n', i, '\n', io)
    
    ground = io[0]
    grids = io[1]
    
    featAA = os.path.join(featDIR, ground)
    rasterAA = os.path.join(storeDIR, grids[0])
    rasterBB = os.path.join(storeDIR, grids[1])
    rasterCC = os.path.join(storeDIR, grids[2])
    rasterDD = os.path.join(elevDIR, grids[3])
    
    featA = os.path.join(dataDIR, ground)
    rasterA = os.path.join(dataDIR, grids[0])
    rasterB = os.path.join(dataDIR, grids[1])
    rasterC = os.path.join(dataDIR, grids[2])
    rasterD = os.path.join(dataDIR, grids[3])
    
    shutil.copyfile(featAA, featA)
    shutil.copyfile(rasterAA, rasterA)
    shutil.copyfile(rasterBB, rasterB)
    shutil.copyfile(rasterCC, rasterC)
    shutil.copyfile(rasterDD, rasterD)

    mo = 1 + int((i)/9)
    yrs_i = int((i) % 9)
    yrs = year_labels[yrs_i]
    
    if yrs == '_1974_2013_':
      
      arcpy.management.XYTableToPoint(
        in_table=featA,
        out_feature_class=os.path.join(gdbDIR, 'MX5P_{}_XYTableToPoint'.format(mo)),
        x_field='x',
        y_field='y',
        z_field=None,
        coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision'
      )
  
      arcpy.stats.Forest(
        prediction_type='TRAIN',
        in_features=os.path.join(gdbDIR, 'MX5P_{}_XYTableToPoint'.format(mo)),
        variable_predict='data',
        treat_variable_as_categorical=None,
        explanatory_variables=None,
        distance_features=None,
        explanatory_rasters='DEM.tif #;srad_1974_2013_{}.tif #;tmax_1974_2013_{}.tif #;accm_1974_2013_{}.tif #'.format(mo, mo, mo),
        features_to_predict=None,
        output_features=None,
        output_raster=None,
        output_trained_features=None,
        output_importance_table=None,
        use_raster_values='TRUE',
        number_of_trees=100,
        minimum_leaf_size=5,
        maximum_depth=10,
        sample_size=100,
        random_variables=None,
        percentage_for_training=10,
        output_classification_table=None,
        output_validation_table=None,
        number_validation_runs=10,
        calculate_uncertainty='FALSE',
        output_trained_model=os.path.join(dataDIR, 'TrainedModel.ssm'),
        model_type='GRADIENT_BOOSTED',
        reg_lambda=1,
        gamma=0,
        eta=0.1,
        max_bins=0,
        optimize='TRUE',
        optimize_algorithm='RANDOM',
        optimize_target='R2',
        num_search=10,
        model_param_setting='NUM_TREES 100 1000 5',
        output_param_tuning_table=None
      )
    
      message = arcpy.GetMessages()
      os.remove(os.path.join(dataDIR, 'TrainedModel.ssm'))
      message_part2 = message.split('was approximately reached at seed')[1]
      seed_str = message_part2.split('\n')[0].lstrip()
      n_trees = int([s.split()[-1] for s in message.split('\n') if s[:15] == 'Number of Trees'][0])
      
      arcpy.env.randomGenerator = '{} ACM599'.format(seed_str)
    
      arcpy.stats.Forest(
        prediction_type='TRAIN',
        in_features=os.path.join(gdbDIR, 'MX5P_{}_XYTableToPoint'.format(mo)),
        variable_predict='data',
        treat_variable_as_categorical=None,
        explanatory_variables=None,
        distance_features=None,
        explanatory_rasters='DEM.tif #;srad_1974_2013_{}.tif #;tmax_1974_2013_{}.tif #;accm_1974_2013_{}.tif #'.format(mo, mo, mo),
        features_to_predict=None,
        output_features=None,
        output_raster=None,
        output_trained_features='GBfeatures',
        output_importance_table=None,
        use_raster_values='TRUE',
        number_of_trees=n_trees,
        minimum_leaf_size=5,
        maximum_depth=10,
        sample_size=100,
        random_variables=None,
        percentage_for_training=10,
        output_classification_table=None,
        output_validation_table=None,
        number_validation_runs=1,
        calculate_uncertainty='FALSE',
        output_trained_model=os.path.join(dataDIR, 'TrainedModel.ssm'),
        model_type='GRADIENT_BOOSTED',
        reg_lambda=1,
        gamma=0,
        eta=0.1,
        max_bins=0,
        optimize='FALSE'
      )
    
      arcpy.conversion.ExportTable(
        in_table='GBfeatures', 
        out_table=os.path.join(dataDIR, 'GBfeatures_ExportTable.csv'), 
      )
      
      df = pd.read_csv(os.path.join(dataDIR, 'GBfeatures_ExportTable.csv'))
      rmse_diff = np.sqrt(np.mean((df['PREDICTED']-df['DATA'])**2)) 
      pbias_diff = 100*(np.sum(df['DATA'] - df['PREDICTED'])/np.sum(df['DATA']))
      fo.write('MX5P{}{}'.format(yrs, mo) + ',' + str(rmse_diff) + ',' + str(pbias_diff) + '\n')
      
    arcpy.stats.PredictUsingSSMFile(
      input_model=os.path.join(dataDIR, 'TrainedModel.ssm'),
      prediction_type='PREDICT_RASTER',
      features_to_predict=None,
      output_raster=os.path.join(gdbDIR, 'MX5P{}{}'.format(yrs, mo)),
      explanatory_rasters_matching='DEM.tif DEM false;srad{}{}.tif SRAD_1974_2013_{} false;tmax{}{}.tif TMAX_1974_2013_{} false;accm{}{}.tif ACCM_1974_2013_{} false'.format(yrs, mo, mo, yrs, mo, mo, yrs, mo, mo)
    )
  
    arcpy.management.Delete(os.path.join(gdbDIR, 'MX5P_{}_XYTableToPoint'.format(mo)))
    arcpy.management.Delete('GBfeatures.dbf')
    arcpy.management.Delete('GBfeatures_ExportTable.csv')
    os.remove(featA)
    os.remove(rasterD)
    
    if yrs != '_1974_2013_':
      os.remove(rasterA)
      os.remove(rasterB)
      os.remove(rasterC)
    else:
      a, b, c = [rasterA, rasterB, rasterC]
    
    if yrs == '_2070_2099_':
      os.remove(os.path.join(dataDIR, 'TrainedModel.ssm'))
      os.remove(a)
      os.remove(b)
      os.remove(c)
