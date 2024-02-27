var path = 'NASA/NEX-DCP30'; //'pr kg/m^2/s'
var model = 'CCSM4';
var ic = ee.ImageCollection(path);

var bounds = ic.geometry().bounds();
var proj = ic.first().projection();

var ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]);
var order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);

var modelfilter = ee.Filter.or(
                  ee.Filter.eq('scenario', 'historical'),
                  ee.Filter.eq('scenario', 'rcp45'));

var start = ee.Date.fromYMD(1974, 1, 1);
var end = ee.Date.fromYMD(ee.Number(1974).add(40), 1, 1);
var ref_ic = ic.filterDate(start, end);
var ref_ic = ref_ic.filter(ee.Filter.eq('model', model))
                .filter(modelfilter)
                .select('pr');

function month_fn(month){
  var mo_im = ref_ic.filter(ee.Filter.calendarRange(month, month,'month'))
                .sum().multiply(86400).divide(40)
                .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))));
  return mo_im;
}
var ref_im = ee.ImageCollection(order_months.map(month_fn)).sum();

var start = ee.Date.fromYMD(2070, 1, 1);
var end = ee.Date.fromYMD(ee.Number(2070).add(30), 1, 1);
var nex_ic = ic.filterDate(start, end);
var nex_ic = nex_ic.filter(ee.Filter.eq('model', model))
                .filter(modelfilter)
                .select('pr');

function mmmonth_fn(month){
  var mo_im = nex_ic.filter(ee.Filter.calendarRange(month, month,'month'))
                .sum().multiply(86400).divide(30)
                .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))));
  return mo_im;
}
var nex_im = ee.ImageCollection(order_months.map(mmmonth_fn)).sum();

var diff_im = nex_im.subtract(ref_im);

var perc_diff_im = diff_im.divide(ref_im).multiply(100.0);

var visParam = {min:0, 
                max:800,
                bands:['pr'],
                palette:['blue', 'purple', 'cyan', 'green', 'yellow', 'red']};

Map.addLayer(ref_im, visParam, 'Historical');
Map.addLayer(nex_im, visParam, 'Future');

var visParam = {min:-20, 
                max:80,
                bands:['pr'],
                palette:['blue', 'purple', 'cyan', 'green', 'yellow', 'red']};


var vis_im = diff_im.visualize(visParam);
Map.addLayer(vis_im, null, 'Difference');

function makeColorBarParams(palette) {
  return {
    bbox:[visParam.min, 0, visParam.max, 0.1],
    dimensions:'100x10',
    format:'png',
    min:visParam.min,
    max:visParam.max,
    palette:visParam.palette,
  };
}

var colorBar = ui.Thumbnail({
  image:ee.Image.pixelLonLat().select(0),
  params:makeColorBarParams(visParam.palette),
  style:{position: 'bottom-left', stretch: 'horizontal', margin: '0px 8px', maxHeight: '24px'},
});

var legendLabels = ui.Panel({
  widgets:[
    ui.Label(visParam.min, {margin: '4px 8px'}),
    ui.Label(
    ((visParam.max-visParam.min) / 4+visParam.min),
    {margin: '4px 8px', textAlign: 'center', stretch: 'horizontal'}),
    ui.Label(
        ((visParam.max-visParam.min) / 2+visParam.min),
        {margin: '4px 8px', textAlign: 'center', stretch: 'horizontal'}),
    ui.Label(
    ((visParam.max-visParam.min) / (4/3)+visParam.min),
    {margin: '4px 8px', textAlign: 'center', stretch: 'horizontal'}),
    ui.Label(visParam.max, {margin: '4px 8px'})
  ],
  layout:ui.Panel.Layout.flow('horizontal')
});

var legendTitle = ui.Label({
  value:'2070-2100 annual precip. relative to historical (mm)',
  style:{fontWeight: 'bold'}
});

var legendPanel = ui.Panel([legendTitle, colorBar, legendLabels]);

print(legendPanel);

/*
var geometry = ee.Geometry.Rectangle([-126, 22, -66, 50]);
var thumbnail = vis_im.getThumbURL({
  min:visParam.min,
  max:visParam.max,
  dimensions:1000,
  region:geometry,
  format:'png'
});

print(thumbnail);
*/


var visParam = {min:-15, 
                max:15,
                bands:['pr'],
                palette:['blue', 'purple', 'cyan', 'green', 'yellow', 'red']};


var vis_im = perc_diff_im.visualize(visParam);
Map.addLayer(vis_im, null, 'Percent Difference');


function makeColorBarParams(palette) {
  return {
    bbox:[visParam.min, 0, visParam.max, 0.1],
    dimensions:'100x10',
    format:'png',
    min:visParam.min,
    max:visParam.max,
    palette:visParam.palette,
  };
}

var colorBar = ui.Thumbnail({
  image:ee.Image.pixelLonLat().select(0),
  params:makeColorBarParams(visParam.palette),
  style:{position: 'bottom-left', stretch: 'horizontal', margin: '0px 8px', maxHeight: '24px'},
});

var legendLabels = ui.Panel({
  widgets:[
    ui.Label(visParam.min, {margin: '4px 8px'}),
    ui.Label(
    ((visParam.max-visParam.min) / 4+visParam.min),
    {margin: '4px 8px', textAlign: 'center', stretch: 'horizontal'}),
    ui.Label(
        ((visParam.max-visParam.min) / 2+visParam.min),
        {margin: '4px 8px', textAlign: 'center', stretch: 'horizontal'}),
    ui.Label(
    ((visParam.max-visParam.min) / (4/3)+visParam.min),
    {margin: '4px 8px', textAlign: 'center', stretch: 'horizontal'}),
    ui.Label(visParam.max, {margin: '4px 8px'})
  ],
  layout:ui.Panel.Layout.flow('horizontal')
});

var legendTitle = ui.Label({
  value:'2070-2100 annual precip. relative to historical (%Change)',
  style:{fontWeight: 'bold'}
});

var legendPanel = ui.Panel([legendTitle, colorBar, legendLabels]);

print(legendPanel);


Map.addLayer(ee.FeatureCollection('users/andrewfullhart/SW_Study_Area'), null, 'Area');
