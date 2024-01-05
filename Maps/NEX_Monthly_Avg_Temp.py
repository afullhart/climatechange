import time
import ee
ee.Initialize()

path = 'NASA/NEX-DCP30'
model = 'CCSM4'
out_dir = 'users/andrewfullhart/'

ic = ee.ImageCollection(path)
bounds = ic.geometry().bounds()
proj = ic.first().projection()
start_year = 1974
end_year = 2013
start = ee.Date.fromYMD(start_year, 1, 1)
end = ee.Date.fromYMD(end_year, 12, 31)

ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

modelfilter = ee.Filter.Or(
              ee.Filter.eq('scenario', 'historical'),
              ee.Filter.eq('scenario', 'rcp45'))

ic = ic.filterDate(start, end)

ic = ic.filter(ee.Filter.eq('model', model))                                    \
       .filter(modelfilter)                                                     \
       .select('tasmax')

def month_fn(month):

  mo_im = ic.filter(ee.Filter.calendarRange(month, month,'month'))              \
            .sum().divide(40).multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))))    \

  mo_im = mo_im.expression('(tmax - 273.15)*(1.8)+32', {'tmax':mo_im.select('tasmax')})

  return mo_im

im_list = order_months.map(month_fn)

for i in range(12):
  m = i + 1
  task = ee.batch.Export.image.toAsset(image=ee.Image(im_list.get(i))
                                .rename(['tmax_' + str(m)]),
                        description='tmax_' + str(m) + '_1974_2013',
                        assetId=out_dir + 'tmax_' + str(m) + '_1974_2013',
                        region=bounds,
                        scale=proj.nominalScale().getInfo(),
                        crsTransform=[0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                        crs='EPSG:4326',
                        maxPixels=1e13)

  task.start()


asset_list = ['users/andrewfullhart/tmax_1_1974_2013',
              'users/andrewfullhart/tmax_2_1974_2013',
              'users/andrewfullhart/tmax_3_1974_2013',
              'users/andrewfullhart/tmax_4_1974_2013',
              'users/andrewfullhart/tmax_5_1974_2013',
              'users/andrewfullhart/tmax_6_1974_2013',
              'users/andrewfullhart/tmax_7_1974_2013',
              'users/andrewfullhart/tmax_8_1974_2013',
              'users/andrewfullhart/tmax_9_1974_2013',
              'users/andrewfullhart/tmax_10_1974_2013',
              'users/andrewfullhart/tmax_11_1974_2013',
              'users/andrewfullhart/tmax_12_1974_2013']


timer_condition = True
while timer_condition is True:
  timer_condition = False
  for a in asset_list:
    try:
      ee.data.getAsset(a)
    except ee.EEException:
      timer_condition = True
      break

  time.sleep(5)


for i in range(12):
  m = i + 1
  task = ee.batch.Export.image.toDrive(image=ee.Image(asset_list[i]),
                        description='tmax_1974_2013_' + str(m),
                        folder='GEE_Downloads',
                        region=bounds,
                        scale=proj.nominalScale().getInfo(),
                        crsTransform=[0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                        crs='EPSG:4326',
                        maxPixels=1e9)

  task.start()
