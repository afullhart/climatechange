
var jan = ee.Image('users/andrewfullhart/spei12mo_1_1974_2013'),
    feb = ee.Image('users/andrewfullhart/spei12mo_2_1974_2013'),
    mar = ee.Image('users/andrewfullhart/spei12mo_3_1974_2013'),
    apr = ee.Image('users/andrewfullhart/spei12mo_4_1974_2013'),
    may = ee.Image('users/andrewfullhart/spei12mo_5_1974_2013'),
    jun = ee.Image('users/andrewfullhart/spei12mo_6_1974_2013'),
    jul = ee.Image('users/andrewfullhart/spei12mo_7_1974_2013'),
    aug = ee.Image('users/andrewfullhart/spei12mo_8_1974_2013'),
    sep = ee.Image('users/andrewfullhart/spei12mo_9_1974_2013'),
    oct = ee.Image('users/andrewfullhart/spei12mo_10_1974_2013'),
    nov = ee.Image('users/andrewfullhart/spei12mo_11_1974_2013'),
    dec = ee.Image('users/andrewfullhart/spei12mo_12_1974_2013');

var proj=jan.projection();
var bounds = jan.geometry().bounds();

var img_list = ee.List( [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec] );

for (var i=0; i < 12; i++) {
  var m = i + 1;
  Export.image.toDrive({image:img_list.get( i ), 
                        description: 'spei_1974_2013_' + m,
                        folder: 'GEE_Downloads',
                        region: bounds, 
                        scale: proj.nominalScale().getInfo(), 
                        crsTransform: [0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                        crs: 'EPSG:4326',
                        maxPixels: 1e9});
}
