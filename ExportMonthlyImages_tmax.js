
var jan = ee.Image('users/andrewfullhart/tmax_1_1974_2013'),
    feb = ee.Image('users/andrewfullhart/tmax_2_1974_2013'),
    mar = ee.Image('users/andrewfullhart/tmax_3_1974_2013'),
    apr = ee.Image('users/andrewfullhart/tmax_4_1974_2013'),
    may = ee.Image('users/andrewfullhart/tmax_5_1974_2013'),
    jun = ee.Image('users/andrewfullhart/tmax_6_1974_2013'),
    jul = ee.Image('users/andrewfullhart/tmax_7_1974_2013'),
    aug = ee.Image('users/andrewfullhart/tmax_8_1974_2013'),
    sep = ee.Image('users/andrewfullhart/tmax_9_1974_2013'),
    oct = ee.Image('users/andrewfullhart/tmax_10_1974_2013'),
    nov = ee.Image('users/andrewfullhart/tmax_11_1974_2013'),
    dec = ee.Image('users/andrewfullhart/tmax_12_1974_2013');

var proj=jan.projection();

var img_list = ee.List( [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec] );

for (var i=0; i < 12; i++) {
  var m = i + 1;
  Export.image.toDrive({image:img_list.get( i ), 
                        description:'tmax_1974_2013_' + m,
                        folder:'GEE_Downloads',
                        scale:proj.nominalScale().getInfo(), 
                        crsTransform: [0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                        crs: 'EPSG:4326',
                        maxPixels:1e9});
}
