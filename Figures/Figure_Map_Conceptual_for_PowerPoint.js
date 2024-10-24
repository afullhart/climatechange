
var prVisA = {
  min: 1.0,
  max: 5.0,
  opacity:0.6,
  palette: ['blue', 'purple', 'cyan', 'green', 'yellow', 'red'],
};

var dataset = ee.ImageCollection('NASA/NEX-DCP30')
                  .filter(ee.Filter.date('2018-06-30', '2018-07-31'));
var dataset = dataset.filter(ee.Filter.eq('scenario', 'rcp45'));
var dataset = dataset.filter(ee.Filter.eq('model', 'CCSM4'));
var pr_mo_im = dataset.first().select('pr').multiply(86400);
var pr_mo_viz_im = pr_mo_im.visualize(prVisA);

var prVisB = {
  min: 1.5,
  max: 5.0,
  opacity:0.6,
  palette:['001137', '01abab', 'e7eb05', '620500'],
};

var dataset = ee.ImageCollection('IDAHO_EPSCOR/MACAv2_METDATA')
                  .filter(ee.Filter.date('2018-06-30', '2018-07-31'));
var dataset = dataset.filter(ee.Filter.eq('scenario', 'rcp45'));
var dataset = dataset.filter(ee.Filter.eq('model', 'CCSM4'));
var pr_dy_im = dataset.select('pr').reduce(ee.Reducer.mean());
var pr_dy_viz_im = pr_dy_im.visualize(prVisB);

var prVisC = {
  min: 1.0,
  max: 5.0,
  opacity:0.6,
  palette:'0000aa,0000ff,00aaff,00ffff,aaff55,ffffff,ffff00,fcd37f,ffaa00,e60000,730000',
};

var dataset = ee.ImageCollection('NASA/NEX-DCP30')
                  .filter(ee.Filter.date('2018-06-30', '2018-07-31'));
var dataset = dataset.filter(ee.Filter.eq('scenario', 'rcp45'));
var dataset = dataset.filter(ee.Filter.eq('model', 'CCSM4'));
var pr_par_im = dataset.first().select('pr').multiply(86400);
var pr_par_viz_im = pr_par_im.visualize(prVisC);


Map.setCenter(-110.97, 32.254, 10);
Map.addLayer(pr_par_im, prVisC, 'pars');
Map.addLayer(pr_dy_im, prVisB, 'daily');
Map.addLayer(pr_mo_im, prVisA, 'monthly');


Export.image.toDrive({
  image:pr_dy_viz_im, 
  description:'ImageDaily',
  folder:'GEE_Downloads',
  scale:2000,
  maxPixels:1e10
});

Export.image.toDrive({
  image:pr_mo_viz_im, 
  description:'ImageMonthly',
  folder:'GEE_Downloads',
  scale:400,
  maxPixels:1e10
});

Export.image.toDrive({
  image:pr_par_viz_im, 
  description:'ImagePars',
  folder:'GEE_Downloads',
  scale:400,
  maxPixels:1e10
});
