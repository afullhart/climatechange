var path = 'users/gponce/usda_ars/image_collections/prism800m_spei_s12'; //'b1'

var dataset = ee.ImageCollection(path).select('b1');
var bounds = dataset.geometry().bounds();
var proj=dataset.first().projection();
var start_year = 1974;
var end_year = 2013;
var years = ee.List.sequence(start_year, end_year);
var months = ee.List.sequence(1, 12);

var ic_monthly =  ee.ImageCollection.fromImages(
  years.map(function(y) {
      return months.map(function(m) {
        var v_start = ee.Date.fromYMD(y, m, 1).update({hour:7});
        var month_image = dataset.filterDate(v_start).first();
        return month_image
               .set('year', y)
               .set('month', m)
               .set('system:time_start', ee.Date.fromYMD(y, m, 1).millis());
      });
    }).flatten()
  );

var results = 
  months.map(function (m) {
    var month_image = ic_monthly
                      .filter(ee.Filter.calendarRange(m, m, 'month'))
                      .mean()
                      .rename(ee.String('spei12mo_').cat(ee.Number(m).format('%02d')));
    return ee.Image(month_image);
  });

var out_dir = 'users/andrewfullhart/';

for (var i = 0; i < 12; i++) {
  var m = i + 1;
  Export.image.toAsset({image:ee.Image(results.get(i))
                                    .rename(['spei12mo_'+ m]), 
                        description: 'spei12mo_' + m + '_1974_2013', 
                        assetId: out_dir + 'spei12mo_' + m + '_1974_2013',
                        region: bounds, 
                        scale: proj.nominalScale().getInfo(), 
                        crsTransform: [0.00833333333, 0, -125.02083333, 0, 0.00833333333, 24.0625],
                        crs: 'EPSG:4326',
                        maxPixels: 1e13});
}



