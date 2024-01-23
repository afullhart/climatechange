var path = 'NASA/NEX-DCP30'; //'pr kg/m^2/s'
var nex_set = ee.ImageCollection(path);

var path = 'users/gponce/usda_ars/image_collections/prism800m_monthly_precipitation'; //'b1'
var ref_set = ee.ImageCollection(path).select('b1');

var study_area = ee.FeatureCollection('users/andrewfullhart/SW_Study_Area');

var model_list = ee.List(['ACCESS1-0', 'bcc-csm1-1', 'BNU-ESM', 'CanESM2', 'CCSM4', 'CESM1-BGC', 'CNRM-CM5', 'CSIRO-Mk3-6-0', 'GFDL-CM3', 'GFDL-ESM2G', 'GFDL-ESM2M', 'inmcm4', 'IPSL-CM5A-LR', 'IPSL-CM5A-MR', 'MIROC-ESM', 'MIROC-ESM-CHEM', 'MIROC5', 'MPI-ESM-LR', 'MPI-ESM-MR', 'MRI-CGCM3', 'NorESM1-M']);

var bounds = ref_set.geometry().bounds();
var proj = ref_set.first().projection();
var start_year = 1974;
var end_year = 2013;
var start = ee.Date.fromYMD(start_year, 1, 1);
var end = ee.Date.fromYMD(end_year+1, 1, 1);

var ref_im = ref_set.filterDate(start, end).sum().divide(40);

var ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]);
var order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);

var modelfilter = ee.Filter.or(
                  ee.Filter.eq('scenario', 'historical'),
                  ee.Filter.eq('scenario', 'rcp45'));

var nex_set = nex_set.filter(modelfilter);

function model_fn(model){
  
  var ic = nex_set.filter(ee.Filter.eq('model', model))
                  .filter(modelfilter)
                  .select('pr');

  var start_nested = ee.Date.fromYMD(1974, 1, 1);
  var end_nested = ee.Date.fromYMD(2014, 1, 1);
  var ic_nested = ic.filterDate(start_nested, end_nested);
  function month_fn(month){
    var mo_im = ic_nested.filter(ee.Filter.calendarRange(month, month,'month'))
                  .sum().multiply(86400).divide(40)
                  .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))));
    return mo_im;
  }
  var ann_im = ee.ImageCollection(order_months.map(month_fn)).sum();
  var diff_im = ann_im.subtract(ref_im).divide(ref_im).multiply(100);
  var klip_im = diff_im.clip(study_area);
  
  var mean_dict = klip_im.reduceRegion({
    reducer:ee.Reducer.mean(),
    geometry:study_area.geometry(),
    scale:500,
    maxPixels:1e10
  });
  var avg_rel = mean_dict.get('pr');
  
  var diff_im = ann_im.subtract(ref_im).pow(2).pow(0.5).divide(ref_im).multiply(100);
  var klip_im = diff_im.clip(study_area);
  var mean_dict = klip_im.reduceRegion({
    reducer:ee.Reducer.mean(),
    geometry:study_area.geometry(),
    scale:500,
    maxPixels:1e10
  });
  var avg_abs = mean_dict.get('pr');
  
  return ee.Feature(null, {model:model, avg_abs:avg_abs, avg_rel:avg_rel});
}

var out_fc = ee.FeatureCollection(model_list.map(model_fn));

Export.table.toDrive({collection:out_fc, 
                      description:'PRISM_NEX_PRECIP_DIFF_HISTORICAL',
                      folder:'GEE_Downloads',
                      selectors:['model', 'avg_abs', 'avg_rel']});
