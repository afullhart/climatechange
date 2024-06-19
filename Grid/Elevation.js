var nex_im = ee.ImageCollection('NASA/NEX-DCP30').first();
var scale = nex_im.projection().nominalScale().getInfo();

var ROI = ee.Geometry.Rectangle([-121, 30, -102, 43], 'EPSG:4326', false);

var L8proj = ee.ImageCollection('JAXA/ALOS/AW3D30/V3_2')
        .filterBounds(ROI).first().projection();
var im = ee.ImageCollection('JAXA/ALOS/AW3D30/V3_2').select('DSM').mosaic().setDefaultProjection(L8proj);

var proj = nex_im.projection().getInfo();

var transform = [
  proj.transform[0],
  proj.transform[1],
  proj.transform[2],
  proj.transform[3],
  proj.transform[4],
  proj.transform[5],
];

var transform_new = [
  0.0083333333,
  proj.transform[1],
  proj.transform[2],
  proj.transform[3],
  0.0083333333,
  proj.transform[5],
];

var proj = nex_im.projection();

var eimage = im;
var eimage = eimage.resample('bilinear').reproject({crs:proj.crs(), crsTransform:transform_new});
var eimage = eimage.clip(ROI);

Map.addLayer(eimage);

Export.image.toDrive({
  image:eimage,
  description:'DEM',
  folder:'GEE_Downloads',
  region:ROI,
  scale:scale,
  crs:'EPSG:4326',
  maxPixels:1e13});
  
  
