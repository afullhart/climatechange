var petAvg = ee.Image('users/andrewfullhart/pet_1974_2013');
var proj = petAvg.projection();
var bounds = petAvg.geometry().bounds();

Export.image.toDrive({image: petAvg,
                      description: 'pet_1974_2013',
                      folder: 'GEE_Downloads',
                      region: bounds, 
                      scale: proj.nominalScale().getInfo(), 
                      crsTransform: [0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                      crs: 'EPSG:4326',
                      maxPixels: 1e13});
