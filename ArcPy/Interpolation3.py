import shutil
import os
import arcpy


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



#for i, io in enumerate(map_io_data):
for i, io in enumerate(map_io_data[:1]):
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
  if mo == 1:
    
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
      explanatory_variable_matching=None,
      explanatory_distance_matching=None,
      explanatory_rasters_matching=None,
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
      compensate_sparse_categories='FALSE',
      number_validation_runs=5,
      calculate_uncertainty='FALSE',
      output_trained_model=os.path.join(dataDIR, 'TrainedModel.ssm'),
      model_type='GRADIENT_BOOSTED',
      reg_lambda=1,
      gamma=0,
      eta=0.3,
      max_bins=0,
      optimize='TRUE',
      optimize_algorithm='RANDOM',
      optimize_target='R2',
      num_search=5,
      model_param_setting='NUM_TREES 100 1000 5',
      output_param_tuning_table=None,
      include_probabilities='HIGHEST_PROBABILITY_ONLY'
    )
  
  arcpy.stats.PredictUsingSSMFile(
    input_model=os.path.join(dataDIR, 'TrainedModel.ssm'),
    prediction_type='PREDICT_RASTER',
    features_to_predict=None,
    output_features=None,
    output_raster=os.path.join(gdbDIR, 'MX5P{}{}'.format(yrs, mo)),
    explanatory_variable_matching=None,
    explanatory_distance_matching=None,
    explanatory_rasters_matching='DEM.tif DEM false;srad{}{}.tif SRAD{}{} false;tmax{}{}.tif TMAX{}{} false;accm{}{}.tif ACCM{}{} false'.format(yrs, mo, yrs, mo, yrs, mo, yrs, mo, yrs, mo, yrs, mo)
  )
  
  arcpy.management.Delete(os.path.join(gdbDIR, 'MX5P_{}_XYTableToPoint'.format(mo)))
  os.remove(os.path.join(dataDIR, 'TrainedModel.ssm'))
  os.remove(featA)
  os.remove(rasterA)
  os.remove(rasterB)
  os.remove(rasterC)
  os.remove(rasterD)
  

