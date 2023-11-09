var path = 'NASA/NEX-DCP30'; //'pr kg/m^2/s'
var nex_set = ee.ImageCollection(path);

var path = 'users/gponce/usda_ars/image_collections/prism800m_monthly_precipitation'; //'b1'
var pri_set = ee.ImageCollection(path).select('b1');

var bounds = pri_set.geometry().bounds();
var proj = pri_set.first().projection();
var start_year = 1974;
var end_year = 2013;
var start = ee.Date.fromYMD(start_year, 1, 1);
var end = ee.Date.fromYMD(end_year, 12, 31);

var pri_im = pri_set.filterDate(start, end).sum().divide(40);

var ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]);
var order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);

var modelfilter = ee.Filter.or(
                  ee.Filter.eq('scenario', 'historical'),
                  ee.Filter.eq('scenario', 'rcp45'));

var ic = nex_set.filter(ee.Filter.eq('model', 'CESM1-BGC'))
                .filter(modelfilter)
                .select('pr');

var start = ee.Date.fromYMD(2070, 1, 1);
var end = ee.Date.fromYMD(ee.Number(2070).add(29), 12, 31);
var ic = ic.filterDate(start, end);
function month_fn(month){
  var mo_im = ic.filter(ee.Filter.calendarRange(month, month,'month'))
                .sum().multiply(86400).divide(30)
                .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))));
  return mo_im;
}
var ann_im = ee.ImageCollection(order_months.map(month_fn)).sum();

var diff_im = ann_im.subtract(pri_im);
var visParam = {min:-100, 
                max:300,
                bands:['pr'],
                palette:['#ff355e','#fd5b78','#ff6037','#ff9966','#ff9933','#ffcc33','#ffff66','#ccff00','#66ff66','#aaf0d1','#16d0cb','#50bfe6','#9c27b0','#ee34d2','#ff00cc']};

var vis_im = diff_im.visualize(visParam);
Map.addLayer(vis_im);

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
        ((visParam.max-visParam.min) / 2+visParam.min),
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

var geometry = ee.Geometry.Rectangle([-126, 22, -66, 50]);

var thumbnail = vis_im.getThumbURL({
  min:visParam.min,
  max:visParam.max,
  dimensions:1000,
  region:geometry,
  format:'png'
});

print(thumbnail);
print(legendPanel);
