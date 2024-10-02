
var prVis = {
  min: 1.0,
  max: 5.0,
  opacity:0.6,
  palette: ['blue', 'purple', 'cyan', 'green', 'yellow', 'red'],
};


var dataset = ee.ImageCollection('NASA/NEX-DCP30')
                  .filter(ee.Filter.date('2018-06-30', '2018-07-31'));

var dataset = dataset.filter(ee.Filter.eq('scenario', 'rcp45'));
var dataset = dataset.filter(ee.Filter.eq('model', 'CCSM4'));
//var pr_im = dataset.select('pr').reduce(ee.Reducer.mean()).multiply(86400);
var pr_mo_im = dataset.first().select('pr').multiply(86400);
var pr_mo_viz_im = pr_mo_im.visualize(prVis);



var dataset = ee.ImageCollection('IDAHO_EPSCOR/MACAv2_METDATA')
                  .filter(ee.Filter.date('2018-06-30', '2018-07-31'));

var dataset = dataset.filter(ee.Filter.eq('scenario', 'rcp45'));
var dataset = dataset.filter(ee.Filter.eq('model', 'CCSM4'));
var pr_dy_im = dataset.select('pr').reduce(ee.Reducer.mean());
var pr_dy_viz_im = pr_dy_im.visualize(prVis);


Map.setCenter(-110.97, 32.254, 10);
Map.addLayer(pr_mo_im, prVis, 'monthly');
Map.addLayer(pr_dy_im, prVis, 'daily');
        
Export.image.toDrive({
  image:pr_dy_viz_im, 
  description:'Image2',
  folder:'GEE_Downloads',
  scale:2000,
  maxPixels:1e9
});

