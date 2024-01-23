var path = 'users/gponce/usda_ars/image_collections/prism800m_monthly_precipitation'; //'b1'
var dataset = ee.ImageCollection(path);
//var points = ee.FeatureCollection('users/andrewfullhart/US_CLIGEN_Coords');
var points = ee.FeatureCollection('users/andrewfullhart/GHCNd_Coords');
//var out_description = 'PRISM_USCLIGEN_Map_Sample_Annual_Precip';
var out_description = 'PRISM_GHCNd_Map_Sample_Annual_Precip';


var dataset = ee.ImageCollection(path).select('b1');
var bounds = dataset.geometry().bounds();
var proj = dataset.first().projection();
var start_year = 1974;
var end_year = 2013;
var start = ee.Date.fromYMD(start_year, 1, 1);
var end = ee.Date.fromYMD(end_year+1, 1, 1);

var sum_image = dataset.filterDate(start, end).sum().divide(40);
var sample_fc = sum_image.sampleRegions({collection:points, scale:100});

Export.table.toDrive({collection:sample_fc,
                      description:out_description,
                      selectors:['stationID', 'b1'],
                      folder:'GEE_Downloads'
});
