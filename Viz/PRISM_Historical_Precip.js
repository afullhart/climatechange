var points = ee.FeatureCollection('users/andrewfullhart/GHCNd_Coords');

//var path = 'NASA/NEX-DCP30'; //'pr kg/m^2/s'
//var nex_set = ee.ImageCollection(path);

//Private dataset path
var path = //'b1'
var pri_set = ee.ImageCollection(path).select('b1');

var bounds = pri_set.geometry().bounds();
var proj = pri_set.first().projection();
var start_year = 1974;
var end_year = 2013;
var start = ee.Date.fromYMD(start_year, 1, 1);
var end = ee.Date.fromYMD(end_year+1, 1, 1);

var pri_im = pri_set.filterDate(start, end).sum().divide(40);


var precipitation = pri_im.select('b1');
var precipitationVis = {
  min: 0,
  max: 1000,
  palette: ['blue', 'purple', 'cyan', 'green', 'yellow', 'red'],
};

Map.setCenter(-115.356, 38.686, 5);
Map.addLayer(
    precipitation, precipitationVis, '40-year Precip.');
    
Map.addLayer(points);

var point = ee.Geometry.Point(-112.78, 31.93);
Map.addLayer(point);
