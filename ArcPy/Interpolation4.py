###############################################################################
'MX5P surfaces from gradient boosting'
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
arcpy.env.randomGenerator = '123 ACM599'

var_labels = ['mx5p']
covar_labels = ['accm', 'tmax', 'srad']
year_labels = ['1974_2013', '2000_2029', '2010_2039', '2020_2049', '2030_2059', '2040_2069', '2050_2079', '2060_2089', '2070_2099']

extent = [43.0, -121.0, -102.0, 30.0]

map_io_data = []
for mo in range(1, 13):
  ground = 'MX5P_{}'.format(mo)
  for yrlabel in year_labels:
    covars = [var + '_' + yrlabel + '_' + str(mo) for var in covar_labels]
    map_io_data.append([ground, covars])


with open(os.path.join(dataDIR, 'GB_CV.csv'), 'w') as fo:
  fo.write('map,rmse,pbias,mape\n')
  for i, io in enumerate(map_io_data):
    
    print('\nITERATION INDEX\n', i, '\n', io)
    
    ground = io[0]
    covars = io[1]
    
    
    featAA = os.path.join(featDIR, ground + '.txt')    
    rasterAA = os.path.join(storeDIR, covars[0] + '.tif')
    rasterBB = os.path.join(storeDIR, covars[1] + '.tif')
    rasterCC = os.path.join(storeDIR, covars[2] + '.tif')
    rasterDD = os.path.join(elevDIR, 'DEM.tif')
    
    featA = os.path.join(dataDIR, ground + '.txt')
    rasterA = os.path.join(dataDIR, covars[0] + '.tif')
    rasterB = os.path.join(dataDIR, covars[1] + '.tif')
    rasterC = os.path.join(dataDIR, covars[2] + '.tif')
    rasterD = os.path.join(dataDIR, 'DEM.tif')
    
    shutil.copyfile(featAA, featA)
    shutil.copyfile(rasterAA, rasterA)
    shutil.copyfile(rasterBB, rasterB)
    shutil.copyfile(rasterCC, rasterC)
    shutil.copyfile(rasterDD, rasterD)
    
    mo = 1 + int((i)/9)
    yrs_i = int((i) % 9)
    yrs = year_labels[yrs_i]
    
    outputCoordinateSystem = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
    snapRaster = rasterD
    parallelProcessingFactor = '5'
    extent = '-121.0 30.0 -102.0 43.0 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
    cellSize = rasterD
    
    if yrs == '1974_2013':
      
      arcpy.management.XYTableToPoint(
        in_table=featA,
        out_feature_class=os.path.join(gdbDIR, 'MX5P_{}_XYTableToPoint'.format(mo)),
        x_field='x',
        y_field='y',
        z_field=None,
        coordinate_system='GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision'
      )
      
      with arcpy.EnvManager(outputCoordinateSystem=outputCoordinateSystem, extent=extent, snapRaster=snapRaster, parallelProcessingFactor=parallelProcessingFactor, cellSize=cellSize):

        arcpy.stats.Forest(
          prediction_type='TRAIN',
          in_features=os.path.join(gdbDIR, 'MX5P_{}_XYTableToPoint'.format(mo)),
          variable_predict='data',
          treat_variable_as_categorical=None,
          explanatory_variables=None,
          distance_features=None,
          explanatory_rasters='srad_1974_2013_{}.tif #;tmax_1974_2013_{}.tif #;accm_1974_2013_{}.tif #'.format(mo, mo, mo),
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
          explanatory_rasters='srad_1974_2013_{}.tif #;tmax_1974_2013_{}.tif #;accm_1974_2013_{}.tif #'.format(mo, mo, mo),
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
        mape_diff = 100*(1/df['DATA'].loc[df['DATA'] != 0.0].size)*(np.nansum(np.absolute((df['DATA'] - df['PREDICTED'])/(df['DATA'].replace(0.0, np.nan)))))
                     
        fo.write('mx5p_{}_{}'.format(yrs, mo) + ',' + str(rmse_diff) + ',' + str(pbias_diff) + ',' + str(mape_diff) + '\n')

    with arcpy.EnvManager(outputCoordinateSystem=outputCoordinateSystem, extent=extent, snapRaster=snapRaster, parallelProcessingFactor=parallelProcessingFactor, cellSize=cellSize):

      arcpy.stats.PredictUsingSSMFile(
        input_model=os.path.join(dataDIR, 'TrainedModel.ssm'),
        prediction_type='PREDICT_RASTER',
        features_to_predict=None,
        output_raster=os.path.join(gdbDIR, 'mx5p_{}_{}'.format(yrs, mo)),
        explanatory_rasters_matching='SRAD_{}_{}.tif SRAD_1974_2013_{} false;TMAX_{}_{}.tif TMAX_1974_2013_{} false;ACCM_{}_{}.tif ACCM_1974_2013_{} false'.format(yrs, mo, mo, yrs, mo, mo, yrs, mo, mo)
      )
  
    outExtractByMask = arcpy.sa.ExtractByMask(os.path.join(gdbDIR, 'mx5p_{}_{}'.format(yrs, mo)), maskSHP, 'INSIDE')
    outExtractByMask.save(os.path.join(gdbDIR, 'mx5p_{}_{}'.format(yrs, mo)))

  arcpy.management.Delete(os.path.join(gdbDIR, 'MX5P_{}_XYTableToPoint'.format(mo)))
  arcpy.management.Delete('GBfeatures')
  os.remove(os.path.join(dataDIR, 'GBfeatures_ExportTable.csv'))
  os.remove(featA)
  os.remove(rasterA)
  os.remove(rasterB)
  os.remove(rasterC)
  os.remove(rasterD)
    

for mo in range(1, 13):
  arcpy.management.Delete(os.path.join(gdbDIR, 'MX5P_{}_XYTableToPoint'.format(mo)))

