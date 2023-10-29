var path = 'users/gponce/usda_ars/image_collections/prism800m_monthly_precipitation'; //'b1'

var dataset = ee.ImageCollection(path).select('b1');
var bounds = dataset.geometry().bounds();
var proj = dataset.first().projection();
var start_year = 1974;
var end_year = 2013;
var start_date = ee.Date.fromYMD(start_year, 1, 1);
var end_date = ee.Date.fromYMD(end_year, 1, 1);
var date_range = ee.DateRange(start_date, end_date);

var path = 'IDAHO_EPSCOR/TERRACLIMATE';

var pet_image = ee.ImageCollection(path).filterDate(date_range)
                                      .select('pet')
                                      .mean();

var out_dir = 'users/andrewfullhart/';

Export.image.toAsset({image: pet_image,
                      description: 'pet_1974_2013', 
                      assetId: out_dir + 'pet_1974_2013',
                      region: bounds, 
                      scale: proj.nominalScale().getInfo(), 
                      crsTransform: [0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                      crs: 'EPSG:4326',
                      maxPixels: 1e13});
