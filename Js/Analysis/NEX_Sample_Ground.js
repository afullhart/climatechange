var path = 'NASA/NEX-DCP30'; //'pr kg/m^2/s'
var dataset = ee.ImageCollection(path);
var points = ee.FeatureCollection('users/andrewfullhart/US_CLIGEN_Coords');

var dataset = ee.ImageCollection(path).select('pr');
var bounds = dataset.geometry().bounds();
var proj = dataset.first().projection();
var start_year = 1974;
var end_year = 2013;
var start = ee.Date.fromYMD(start_year, 1, 1);
var end = ee.Date.fromYMD(end_year, 1, 1);
var years = ee.List.sequence(start_year, end_year);

var sum_image = dataset.filterDate(start, end).sum().divide(40).multiply(86400);
print(sum_image);
print(points);
Map.addLayer(sum_image);

var sample_fc = sum_image.sampleRegions(points);
print(sample_fc);

Export.table.toDrive({collection:sample_fc,
                      description:'NEX_USCLIGEN_Map_Sample_Annual_Precip',
                      selectors:['stationID', 'pr'],
                      folder:'GEE_Downloads'
});


