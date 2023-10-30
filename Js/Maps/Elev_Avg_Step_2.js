var elevAvg = ee.Image('users/andrewfullhart/AvgElev3DEP');
var proj = elevAvg.projection();
var bounds = elevAvg.geometry().bounds();

Export.image.toDrive({image: elevAvg,
                      description: 'AvgElev3DEP',
                      folder: 'GEE_Downloads',
                      region: bounds, 
                      scale: proj.nominalScale().getInfo(), 
                      crsTransform: [0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                      crs: 'EPSG:4326',
                      maxPixels: 1e13});
