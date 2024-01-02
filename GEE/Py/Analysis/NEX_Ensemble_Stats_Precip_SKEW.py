import ee
ee.Initialize(project='ee-andrewfullhart')

ic = ee.ImageCollection('NASA/NEX-DCP30')

out_file = '/content/drive/MyDrive/Colab Notebooks/NEX_Ensemble_Stats_Precip_SKEW.csv'

study_area = ee.FeatureCollection('users/andrewfullhart/SW_Study_Area')

model_list = ee.List(['ACCESS1-0', 'bcc-csm1-1', 'BNU-ESM', 'CanESM2', 'CCSM4', 'CESM1-BGC', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'GFDL-CM3', 'GFDL-ESM2G', 'GFDL-ESM2M', 'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'MIROC-ESM', 'MIROC-ESM-CHEM', 'MIROC5', 'MPI-ESM-LR', 'MPI-ESM-MR', 'MRI-CGCM3', 'NorESM1-M'])

ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

reducer_list = ee.List([ee.Reducer.percentile([25]),
                        ee.Reducer.percentile([75]),
                        ee.Reducer.min(),
                        ee.Reducer.max(),
                        ee.Reducer.mean()])


reducer_str_list = ee.List(['pr_skew_p25', 'pr_skew_p75', 'pr_skew_min', 'pr_skew_max', 'pr_skew_mean'])
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

  def window_fn(winyear):

    winstart = ee.Date.fromYMD(ee.Number(winyear), 1, 1)
    winend = ee.Date.fromYMD(ee.Number(winyear).add(29), 12, 31)
    win_ic = ic.filterDate(winstart, winend)
    win_year_list = ee.List.sequence(ee.Number(winyear), ee.Number(winyear).add(29))

    def model_fn(model):

      model_ic = win_ic.filter(ee.Filter.eq('model', model))                    \
                      .select('pr')

      def year_fn(year):

        start = ee.Date.fromYMD(ee.Number(year), 1, 1)
        end = ee.Date.fromYMD(ee.Number(year), 12, 31)
        year_ic = model_ic.filterDate(start, end)

        def month_fn(month):
          mo_im = year_ic.filter(ee.Filter.calendarRange(month, month,'month')).sum()      \
                        .multiply(86400)                                                   \
                        .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))))
          mo_im = mo_im.clip(study_area)
          return mo_im

        ann_im = ee.ImageCollection(order_months.map(month_fn)).sum()
        return ann_im

      skew_im = ee.ImageCollection(win_year_list.map(year_fn)).reduce(ee.Reducer.skew())
      return skew_im

    ensemble_ic = ee.ImageCollection(model_list.map(model_fn))

    def reducer_fn(re_i):
      re_i = ee.Number(re_i)
      re_im = ensemble_ic.reduce(reducer_list.get(re_i))
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

    return out_ft

  ft_list = years_list.map(window_fn)
  ft = ee.Feature(ft_list.get(0))
  print(ft.getInfo())
  dict_list.append(ft.getInfo())

with open(out_file, 'w') as fo:

  fo.write('yr,min,max,q25,q75,avg\n')

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
