import ee
ee.Initialize(project='ee-andrewfullhart')

path = 'NASA/NEX-DCP30'#'tasmax K'
ic = ee.ImageCollection(path)
outFILE = '/content/drive/My Drive/Colab Notebooks/NEX_Regional_1Year_MaxTemp_Tseries.csv'
model_list = ['CCSM4', 'CanESM2', 'MIROC5']
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

out_dict = {}
for model in model_list:

  print(model)

  model_ic = ic.filter(ee.Filter.eq('model', model))                            \
               .filter(modelfilter)                                             \
               .select('tasmax')

  def year_fn(year):

    start = ee.Date.fromYMD(ee.Number(year), 1, 1)
    end = ee.Date.fromYMD(ee.Number(year).add(1), 1, 1)
    year_ic = model_ic.filterDate(start, end)

    def month_fn(month):
      mo_im = year_ic.filter(ee.Filter.calendarRange(month, month,'month'))     \
                    .sum().multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))))    \
                    .divide(365.25)

      return mo_im

    ann_im = ee.ImageCollection(order_months.map(month_fn)).sum()

    mean_dict = ann_im.reduceRegion(
      reducer=ee.Reducer.mean(),
      geometry=study_area.geometry(),
      scale=scale,
      maxPixels=1e10)
    avg_stat = mean_dict.get('tasmax')
    avg_stat = ee.Number(avg_stat).expression('(tmax - 273.15)*(1.8)+32', {'tmax':avg_stat})
    
    return avg_stat
  
  model_precip_list = years_list.map(year_fn)
  out_dict[model] = model_precip_list.getInfo()


with open(outFILE, 'w') as fo:
  fo.write('year,CCSM4,CanESM2,MIROC5\n')
  for i, year in enumerate(years_list.getInfo()):
    fo.write(str(year) + ',')
    values = []
    for model in model_list:
      value = str(out_dict[model][i])
      values.append(value)
    fo.write(','.join(values) + '\n')
