import time
import ee
ee.Initialize()

path = 'users/gponce/usda_ars/image_collections/prism800m_monthly_precipitation'
coarse_image = ee.ImageCollection(path).first()
coarseProjection = coarse_image.projection()
dem_dataset = ee.Image('USGS/3DEP/10m')
elevation = dem_dataset.select('elevation')
bounds = coarse_image.geometry().bounds()

reKwds = {'reducer':ee.Reducer.mean(), 'maxPixels': 65535}

elevAvg = elevation.reduceResolution(**reKwds).reproject(crs=coarseProjection)

out_dir = 'users/andrewfullhart/'

task = ee.batch.Export.image.toAsset(image=elevAvg,
                      description='AvgElev3DEP',
                      assetId=out_dir + 'AvgElev3DEP',
                      region=bounds,
                      scale=coarseProjection.nominalScale().getInfo(),
                      crsTransform=[0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                      crs='EPSG:4326',
                      maxPixels=1e13)

task.start()


timer_condition = True
while timer_condition is True:
  timer_condition = False
  a = 'users/andrewfullhart/AvgElev3DEP'
  try:
    ee.data.getAsset(a)
  except ee.EEException:
    timer_condition = True

  time.sleep(5)


task = ee.batch.Export.image.toDrive(image=elevAvg,
          description='AvgElev3DEP',
          folder='GEE_Downloads',
          region=bounds,
          scale=proj.nominalScale().getInfo(),
          crsTransform=[0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
          crs='EPSG:4326',
          maxPixels=1e13)

task.start()
