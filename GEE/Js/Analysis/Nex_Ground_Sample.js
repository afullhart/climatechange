var path = 'NASA/NEX-DCP30'; //'pr kg/m^2/s'
var dataset = ee.ImageCollection(path);
var points = ee.FeatureCollection('users/andrewfullhart/US_CLIGEN_Coords');

var dataset = ee.ImageCollection(path).select('pr');
var bounds = dataset.geometry().bounds();
var proj = dataset.first().projection();
var start_year = 1974;
var end_year = 2013;
var start = ee.Date.fromYMD(start_year, 1, 1);
var end = ee.Date.fromYMD(end_year, 12, 31);

var models = ['ACCESS1-0', 'bcc-csm1-1', 'BNU-ESM', 'CanESM2', 'CCSM4', 'CESM1-BGC', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'GFDL-CM3', 'GFDL-ESM2G', 'GFDL-ESM2M', 'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'MIROC-ESM', 'MIROC-ESM-CHEM', 'MIROC5', 'MPI-ESM-LR', 'MPI-ESM-MR', 'MRI-CGCM3', 'NorESM1-M'];

var ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]);
var order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);

var modelfilter = ee.Filter.or(
                  ee.Filter.eq('scenario', 'historical'),
                  ee.Filter.eq('scenario', 'rcp45'));

function model_fn(model){
  var ic = dataset.filterDate(start, end)
                  .filter(ee.Filter.eq('model', model))
                  .filter(modelfilter)
                  .select('pr');
  
  function month_fn(month){
    var mo_im = ic.filter(ee.Filter.calendarRange(month, month,'month'))
              .sum().multiply(86400).divide(40)
              .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))));
    return mo_im;
  }
  
  var mo_ic = ee.ImageCollection(order_months.map(month_fn));
  var mo_im = mo_ic.sum();
  var sample_fc = mo_im.sampleRegions(points, ['stationID']);
  var stationID_list = sample_fc.aggregate_array('stationID');
  var precip_list = sample_fc.aggregate_array('pr');
  return ee.Feature(null,{md:model, stationID:stationID_list, pr:precip_list});
}

var out_fc = ee.FeatureCollection(models.map(model_fn));

Export.table.toDrive({collection:out_fc,
                      description:'NEX_USCLIGEN_Map_Sample_Annual_Precip',
                      selectors:['md', 'stationID,', 'pr'],
                      folder:'GEE_Downloads'
});
