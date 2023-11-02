var path = 'users/gponce/usda_ars/image_collections/prism800m_monthly_precipitation'; //'b1'
var dataset = ee.ImageCollection(path);
var points = ee.FeatureCollection('users/andrewfullhart/US_CLIGEN_Coords');

var dataset = ee.ImageCollection(path).select('b1');
var bounds = dataset.geometry().bounds();
var proj = dataset.first().projection();
var start_year = 1974;
var end_year = 2013;
var start = ee.Date.fromYMD(start_year, 1, 1);
var end = ee.Date.fromYMD(end_year, 1, 1);

var sum_image = dataset.filterDate(start, end).sum().divide(40);
Map.addLayer(sum_image);

var sample_fc = sum_image.sampleRegions(points);

Export.table.toDrive({collection:sample_fc,
                      description:'PRISM_USCLIGEN_Map_Sample_Annual_Precip',
                      selectors:['stationID', 'b1'],
                      folder:'GEE_Downloads'
});
