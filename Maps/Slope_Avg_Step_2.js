var path = 'users/gponce/usda_ars/image_collections/prism800m_monthly_precipitation';
var coarse_image = ee.ImageCollection(path).first();
var coarseProjection = coarse_image.projection();
var slope = ee.Image('users/andrewfullhart/SlopeHiRes').select('slope');
var bounds = slope.geometry().bounds();

var slopeAvg = slope
    .reduceResolution({
      reducer: ee.Reducer.mean(),
      maxPixels: 65535
    })
    .reproject({
      crs: coarseProjection
    });

var out_dir = 'users/andrewfullhart/';

Export.image.toAsset({image: slopeAvg,
                      description: 'AvgSlope3DEP',
                      assetId: out_dir + 'AvgSlope3DEP',
                      region: bounds, 
                      scale: coarseProjection.nominalScale().getInfo(), 
                      crsTransform: [0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                      crs: 'EPSG:4326',
                      maxPixels: 1e13});
