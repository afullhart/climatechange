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
end = ee.Date.fromYMD(end_year+1, 1, 1)

ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

modelfilter = ee.Filter.Or(
              ee.Filter.eq('scenario', 'historical'),
              ee.Filter.eq('scenario', 'rcp45'))

ic = ic.filterDate(start, end)

ic = ic.filter(ee.Filter.eq('model', model))                                    \
       .filter(modelfilter)                                                     \
       .select('pr')

def month_fn(month):

  mo_im = ic.filter(ee.Filter.calendarRange(month, month,'month'))              \
                .sum().divide(40).multiply(86400)                               \
                .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))))
  return mo_im

im_list = order_months.map(month_fn)

for i in range(12):
  m = i + 1
  task = ee.batch.Export.image.toAsset(image=ee.Image(im_list.get(i))
                                .rename(['prcp_' + str(m)]),
                        description='prcp_' + str(m) + '_1974_2013',
                        assetId=out_dir + 'prcp_' + str(m) + '_1974_2013',
                        region=bounds,
                        scale=proj.nominalScale().getInfo(),
                        crsTransform=[0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                        crs='EPSG:4326',
                        maxPixels=1e13)

  task.start()


asset_list = ['users/andrewfullhart/prcp_1_1974_2013',
              'users/andrewfullhart/prcp_2_1974_2013',
              'users/andrewfullhart/prcp_3_1974_2013',
              'users/andrewfullhart/prcp_4_1974_2013',
              'users/andrewfullhart/prcp_5_1974_2013',
              'users/andrewfullhart/prcp_6_1974_2013',
              'users/andrewfullhart/prcp_7_1974_2013',
              'users/andrewfullhart/prcp_8_1974_2013',
              'users/andrewfullhart/prcp_9_1974_2013',
              'users/andrewfullhart/prcp_10_1974_2013',
              'users/andrewfullhart/prcp_11_1974_2013',
              'users/andrewfullhart/prcp_12_1974_2013']


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
                        description='prcp_1974_2013_' + str(m),
                        folder='GEE_Downloads',
                        region=bounds,
                        scale=proj.nominalScale().getInfo(),
                        crsTransform=[0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                        crs='EPSG:4326',
                        maxPixels=1e9)

  task.start()
