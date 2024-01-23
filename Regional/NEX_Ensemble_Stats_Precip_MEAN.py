import ee
ee.Initialize(project='ee-andrewfullhart')

ic = ee.ImageCollection('NASA/NEX-DCP30')

out_file = '/content/drive/MyDrive/Colab Notebooks/NEX_Ensemble_Stats_Precip_MEAN.csv'

study_area = ee.FeatureCollection('users/andrewfullhart/SW_Study_Area')

model_list = ee.List(['ACCESS1-0', 'bcc-csm1-1', 'BNU-ESM', 'CanESM2', 'CCSM4', 'CESM1-BGC', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'GFDL-CM3', 'GFDL-ESM2G', 'GFDL-ESM2M', 'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'MIROC-ESM', 'MIROC-ESM-CHEM', 'MIROC5', 'MPI-ESM-LR', 'MPI-ESM-MR', 'MRI-CGCM3', 'NorESM1-M'])
model_order = ee.List.sequence(0, ee.Number(model_list.size()).subtract(1))

ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

reducer_list = ee.List([ee.Reducer.percentile([25]),
                        ee.Reducer.percentile([75]),
                        ee.Reducer.min(),
                        ee.Reducer.max(),
                        ee.Reducer.mean()])

reducer_str_list = ee.List(['pr_p25', 'pr_p75', 'pr_min', 'pr_max', 'pr_mean'])
reducer_order = ee.List.sequence(0, 4)

start_year = 1985
end_year = 2070
global_years_list = ee.List.sequence(start_year, end_year)

modelfilter = ee.Filter.Or(
              ee.Filter.eq('scenario', 'historical'),
              ee.Filter.eq('scenario', 'rcp45'))

ic = ic.filter(modelfilter)

dict_list = []

for year in global_years_list.getInfo():

  print(year)
  start_year = year
  end_year = year
  years_list = ee.List.sequence(start_year, end_year)

  def year_fn(year):

    start = ee.Date.fromYMD(ee.Number(year), 1, 1)
    end = ee.Date.fromYMD(ee.Number(year).add(30), 1, 1)
    year_ic = ic.filterDate(start, end)

    def model_fn(model):

      model_ic = year_ic.filter(ee.Filter.eq('model', model))                     \
                        .select('pr')

      def month_fn(month):
        mo_im = model_ic.filter(ee.Filter.calendarRange(month, month,'month'))    \
                      .sum().multiply(86400).divide(30)                           \
                      .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))))
        mo_im = mo_im.clip(study_area)
        return mo_im

      ann_im = ee.ImageCollection(order_months.map(month_fn)).sum()
      return ann_im

    ann_ic = ee.ImageCollection(model_list.map(model_fn))

    def reducer_fn(re_i):
      re_i = ee.Number(re_i)
      re_im = ann_ic.reduce(reducer_list.get(re_i))
      mean_dict = re_im.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=study_area.geometry(),
        scale=500,
        maxPixels=1e10)
      avg_stat = mean_dict.get(reducer_str_list.get(re_i))
      return avg_stat

    stat_list = reducer_order.map(reducer_fn)

    out_ft = ee.Feature(None,
                        {'year':ee.Number(year),
                        'q25':stat_list.get(0),
                        'q75':stat_list.get(1),
                        'min':stat_list.get(2),
                        'max':stat_list.get(3),
                        'avg':stat_list.get(4)})

    ann_ic_list = ann_ic.toList(model_list.size())
    def reduce_fn(model_i):
      re_im = ee.Image(ann_ic_list.get(ee.Number(model_i)))
      mean_dict = re_im.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=study_area.geometry(),
        scale=500,
        maxPixels=1e10)
      avg_stat = mean_dict.get('pr')
      return avg_stat

    stat_list = model_order.map(reduce_fn)

    out_ft = out_ft.set(ee.Dictionary(model_list.zip(stat_list).flatten()))
    return out_ft

  ft_list = years_list.map(year_fn)

  ft = ee.Feature(ft_list.get(0))
  print(ft.getInfo())
  dict_list.append(ft.getInfo())

with open(out_file, 'w') as fo:

  model_list = model_list.getInfo()

  fo.write('yr,min,max,q25,q75,avg,' + ','.join(model_list) + '\n')

  for d in dict_list:
    yr = str(d['properties']['year'])
    min = str(d['properties']['min'])
    max = str(d['properties']['max'])
    q25 = str(d['properties']['q25'])
    q75 = str(d['properties']['q75'])
    avg = str(d['properties']['avg'])

    fo.write(','.join([yr, min, max, q25, q75, avg]))

    for model in model_list:
      fo.write(',' + str(d['properties'][model]))
    
    fo.write('\n')
