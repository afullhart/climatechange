var slopeAvg = ee.Image('users/andrewfullhart/AvgSlope3DEP');
var proj = slopeAvg.projection();
var bounds = slopeAvg.geometry().bounds();

Export.image.toDrive({image: slopeAvg,
                      description: 'AvgSlope3DEP',
                      folder: 'GEE_Downloads',
                      region: bounds, 
                      scale: proj.nominalScale().getInfo(), 
                      crsTransform: [0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                      crs: 'EPSG:4326',
                      maxPixels: 1e13});
