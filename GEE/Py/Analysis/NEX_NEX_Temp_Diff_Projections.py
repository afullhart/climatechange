import ee
ee.Initialize()

path = 'NASA/NEX-DCP30'#'pr kg/m^2/s'
nex_set = ee.ImageCollection(path)
study_area = ee.FeatureCollection('users/andrewfullhart/SW_Study_Area')
out_description = 'NEX_NEX_TEMP_DIFF_PROJECTION'

#model_list = ['ACCESS1-0', 'bcc-csm1-1', 'BNU-ESM', 'CanESM2', 'CCSM4', 'CESM1-BGC', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'GFDL-CM3', 'GFDL-ESM2G', 'GFDL-ESM2M', 'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'MIROC-ESM', 'MIROC-ESM-CHEM', 'MIROC5', 'MPI-ESM-LR', 'MPI-ESM-MR', 'MRI-CGCM3', 'NorESM1-M'];

model_loop_list = [['ACCESS1-0', 'bcc-csm1-1'],
                  ['BNU-ESM', 'CanESM2'],
                  ['CCSM4', 'CESM1-BGC'],
                  ['CNRM-CM5', 'CSIRO-Mk3-6-0'],
                  ['GFDL-CM3', 'GFDL-ESM2G'],
                  ['GFDL-ESM2M', 'inmcm4'],
                  ['IPSL-CM5A-LR', 'IPSL-CM5A-MR'],
                  ['MIROC-ESM', 'MIROC-ESM-CHEM'],
                  ['MIROC5', 'MPI-ESM-LR'],
                  ['MPI-ESM-MR', 'MRI-CGCM3'],
                  [ 'NorESM1-M']]

bounds = nex_set.geometry().bounds()
proj = nex_set.first().projection()
scale = 500

start_year = 1974
end_year = 2013
start = ee.Date.fromYMD(start_year, 1, 1)
end = ee.Date.fromYMD(end_year, 12, 31)
ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

start_year = 1985
end_year = 2070
years_list = ee.List.sequence(start_year, end_year)

modelfilter = ee.Filter.Or(
              ee.Filter.eq('scenario', 'historical'),
              ee.Filter.eq('scenario', 'rcp45'))

nex_set = nex_set.filter(modelfilter)

for i in range(len(model_loop_list)):

  model_list = ee.List(model_loop_list[i])

  def model_fn(model):

    ic = nex_set.filter(ee.Filter.eq('model', model))                           \
                .filter(modelfilter)                                            \
                .select('tasmax')

    ref_ic = ic.filterDate(start, end)

    def month_fn(month):
      mo_im = ref_ic.filter(ee.Filter.calendarRange(month, month,'month'))      \
                    .sum().divide(30).multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))))    \
                    .divide(365.25)
      mo_im = mo_im.clip(study_area)
      return mo_im

    ref_im = ee.ImageCollection(order_months.map(month_fn)).sum()
    ref_im = ref_im.expression('(tmax - 273.15)*(1.8)+32', {'tmax':ref_im.select('tasmax')})
    
    def year_fn(year):

      start_nested = ee.Date.fromYMD(ee.Number(year), 1, 1)
      end_nested = ee.Date.fromYMD(ee.Number(year).add(29), 12, 31)
      ic_nested = ic.filterDate(start_nested, end_nested)

      def month_fn(month):
        mo_im = ic_nested.filter(ee.Filter.calendarRange(month, month,'month'))    \
                      .sum().divide(30).multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))))    \
                      .divide(365.25)
        mo_im = mo_im.clip(study_area)
        return mo_im

      ann_im = ee.ImageCollection(order_months.map(month_fn)).sum()
      ann_im = ann_im.expression('(tmax - 273.15)*(1.8)+32', {'tmax':ann_im.select('tasmax')})
      klip_im = ann_im.clip(study_area)
      mean_dict = klip_im.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=study_area.geometry(),
        scale=scale,
        maxPixels=1e10)

      avg_prc = mean_dict.get('tmax')

      diff_im = ann_im.subtract(ref_im).divide(ref_im).multiply(100)
      klip_im = diff_im.clip(study_area)
      mean_dict = klip_im.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=study_area.geometry(),
        scale=scale,
        maxPixels=1e10)

      avg_rel = mean_dict.get('tmax')

      diff_im = ann_im.subtract(ref_im).pow(2).pow(0.5).divide(ref_im).multiply(100)
      klip_im = diff_im.clip(study_area)
      mean_dict = klip_im.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=study_area.geometry(),
        scale=scale,
        maxPixels=1e10)

      avg_abs = mean_dict.get('tmax')

      return ee.List([avg_prc, avg_abs, avg_rel])

    avgs_arr = ee.Array(years_list.map(year_fn))
    avg_tmx_list = avgs_arr.slice(1, 0, 1).toList().flatten()
    avg_abs_list = avgs_arr.slice(1, 1, 2).toList().flatten()
    avg_rel_list = avgs_arr.slice(1, 2, 3).toList().flatten()

    return ee.Feature(None, {'model':model, 'avg_tmax':avg_tmx_list, 'avg_abs':avg_abs_list, 'avg_rel':avg_rel_list})

  out_fc = ee.FeatureCollection(model_list.map(model_fn))

  task = ee.batch.Export.table.toDrive(collection=out_fc,
                            description=out_description,
                            folder='GEE_Downloads',
                            selectors=['model', 'avg_tmax', 'avg_abs', 'avg_rel'])

  task.start()
