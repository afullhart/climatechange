var points = ee.FeatureCollection('users/andrewfullhart/US_CLIGEN_Coords');

var path = 'NASA/NEX-DCP30'; //'pr kg/m^2/s'
var dataset = ee.ImageCollection(path);
var bounds = dataset.geometry().bounds();
var proj = dataset.first().projection();
var start_year = 1974;
var end_year = 2013;
var start = ee.Date.fromYMD(start_year, 1, 1);
var end = ee.Date.fromYMD(end_year, 12, 31);

var ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]);
var order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);

var modelfilter = ee.Filter.or(
                  ee.Filter.eq('scenario', 'historical'),
                  ee.Filter.eq('scenario', 'rcp45'));

var ic = dataset.filterDate(start, end)
            .filter(modelfilter)
            .filter(ee.Filter.eq('model', 'CCSM4'))
            .select('pr');

function month_fn(month){
  var mo_im = ic.filter(ee.Filter.calendarRange(month, month,'month'))
                .sum().divide(40).multiply(86400)
                .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))));
  return mo_im;
}

var ann_im = ee.ImageCollection(order_months.map(month_fn)).sum();

var precipitation = ann_im.select('pr');
var precipitationVis = {
  min: 0,
  max: 1000,
  palette: ['blue', 'purple', 'cyan', 'green', 'yellow', 'red'],
};

Map.setCenter(-115.356, 38.686, 5);
Map.addLayer(precipitation, precipitationVis, '40-year Precip.');
Map.addLayer(points);
