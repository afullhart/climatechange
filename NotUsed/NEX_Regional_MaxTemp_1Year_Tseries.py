import os
import ee
ee.Initialize()

path = 'NASA/NEX-DCP30'#'pr kg/m^2/s'
ic = ee.ImageCollection(path)
out_description = 'NEX_Regional_Avg_MaxTemp_Tseries'
model = 'CCSM4' #'CanESM2', 'MIROC5'
study_area = ee.FeatureCollection('users/andrewfullhart/SW_Study_Area')

bounds = ic.geometry().bounds()
proj = ic.first().projection()
scale = 500

ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

start_year = 1985
end_year = 2099
years_list = ee.List.sequence(start_year, end_year)

modelfilter = ee.Filter.Or(
              ee.Filter.eq('scenario', 'historical'),
              ee.Filter.eq('scenario', 'rcp45'))

ic = ic.filter(ee.Filter.eq('model', model))                                    \
       .filter(modelfilter)                                                     \
       .select('tasmax')

def year_fn(year):

  start = ee.Date.fromYMD(ee.Number(year), 1, 1)
  end = ee.Date.fromYMD(ee.Number(year), 12, 31)
  year_ic = ic.filterDate(start, end)

  def month_fn(month):
    mo_im = year_ic.filter(ee.Filter.calendarRange(month, month,'month'))       \
                  .sum().multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))))    \
                  .divide(365.25)

    return mo_im

  ann_im = ee.ImageCollection(order_months.map(month_fn)).sum()
  ann_im = ann_im.expression('(tmax - 273.15)*(1.8)+32', {'tmax':ann_im.select('tasmax')})

  mean_dict = ann_im.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=study_area.geometry(),
    scale=scale,
    maxPixels=1e10)
  avg_stat = mean_dict.get('tasmax')

  return ee.Feature(None, {'year':ee.Number(year), 'tmax':avg_stat})


out_fc = ee.FeatureCollection(years_list.map(year_fn))

task = ee.batch.Export.table.toDrive(collection=out_fc,
                          description=out_description,
                          folder='GEE_Downloads',
                          selectors=['year', 'tmax'])

task.start()
