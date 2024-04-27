import ee
ee.Initialize()

path = 'NASA/NEX-DCP30' #'pr kg/m^2/s'
dataset = ee.ImageCollection(path)
points = ee.FeatureCollection('users/andrewfullhart/US_CLIGEN_Coords')
#points = ee.FeatureCollection('users/andrewfullhart/GHCNd_Coords')
out_description = 'NEX_USCLIGEN_Map_Sample_Annual_Precip'
#out_description = 'NEX_GHCNd_Map_Sample_Annual_Precip'

dataset = ee.ImageCollection(path).select('pr')
bounds = dataset.geometry().bounds()
proj = dataset.first().projection()
start_year = 1974
end_year = 2013
start = ee.Date.fromYMD(start_year, 1, 1)
end = ee.Date.fromYMD(end_year+1, 1, 1)

models = ee.List(['ACCESS1-0', 'bcc-csm1-1', 'BNU-ESM', 'CanESM2', 'CCSM4', 'CESM1-BGC', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'GFDL-CM3', 'GFDL-ESM2G', 'GFDL-ESM2M', 'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'MIROC-ESM', 'MIROC-ESM-CHEM', 'MIROC5', 'MPI-ESM-LR', 'MPI-ESM-MR', 'MRI-CGCM3', 'NorESM1-M'])

ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

modelfilter = ee.Filter.Or(
                  ee.Filter.eq('scenario', 'historical'),
                  ee.Filter.eq('scenario', 'rcp45'))

def model_fn(model):
  ic = dataset.filterDate(start, end)                                           \
              .filter(ee.Filter.eq('model', model))                             \
              .filter(modelfilter)                                              \
              .select('pr')

  def month_fn(month):
    mo_im = ic.filter(ee.Filter.calendarRange(month, month,'month'))            \
              .sum().divide(40).multiply(86400)                                 \
              .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))))
    return mo_im

  mo_ic = ee.ImageCollection(order_months.map(month_fn))
  mo_im = mo_ic.sum()
  sample_fc = mo_im.sampleRegions(points, ['stationID'], 100)
  stationID_list = sample_fc.aggregate_array('stationID')
  precip_list = sample_fc.aggregate_array('pr')
  return ee.Feature(None,{'md':model, 'stationID':stationID_list, 'pr':precip_list})

out_fc = ee.FeatureCollection(models.map(model_fn))

task = ee.batch.Export.table.toDrive(collection=out_fc,
                           description=out_description,
                           selectors=['md', 'stationID,', 'pr'],
                           folder='GEE_Downloads')

task.start()
