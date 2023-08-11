var path = 'users/gponce/usda_ars/image_collections/prism800m_monthly_precipitation';
var coarse_image = ee.ImageCollection(path).first();
var coarseProjection = coarse_image.projection();
var dem_dataset = ee.Image('USGS/3DEP/10m');
var elevation = dem_dataset.select('elevation');
var slope = ee.Terrain.slope(elevation);
var bounds = coarse_image.geometry().bounds();

var out_dir = 'users/andrewfullhart/';

Export.image.toAsset({image: slope,
                      description: 'SlopeHiRes',
                      assetId: out_dir + 'SlopeHiRes',
                      region: bounds, 
                      scale: coarseProjection.nominalScale().getInfo(), 
                      crsTransform: [0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                      crs: 'EPSG:4326',
                      maxPixels: 1e13});
