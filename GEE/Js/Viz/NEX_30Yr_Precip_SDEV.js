
var ic = ee.ImageCollection('NASA/NEX-DCP30');

var study_area = ee.FeatureCollection('users/andrewfullhart/SW_Study_Area');

var model = 'CCSM4';

var start_year = 1985;

var ndays_months = ee.List([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]);
var order_months = ee.List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);

var modelfilter = ee.Filter.or(
              ee.Filter.eq('scenario', 'historical'),
              ee.Filter.eq('scenario', 'rcp45'));

var ic = ic.filter(modelfilter);

var winyear = start_year;
var winstart = ee.Date.fromYMD(ee.Number(winyear), 1, 1);
var winend = ee.Date.fromYMD(ee.Number(winyear).add(29), 12, 31);
var win_ic = ic.filterDate(winstart, winend);
var win_year_list = ee.List.sequence(ee.Number(winyear), ee.Number(winyear).add(29));

var model_ic = win_ic.filter(ee.Filter.eq('model', model))                    
                .select('pr');

function year_fn(year){

  var start = ee.Date.fromYMD(ee.Number(year), 1, 1);
  var end = ee.Date.fromYMD(ee.Number(year), 12, 31);
  var year_ic = model_ic.filterDate(start, end);

  function month_fn(month){
    var mo_im = year_ic.filter(ee.Filter.calendarRange(month, month,'month')).sum()     
                  .multiply(86400)                                                   
                  .multiply(ee.Number(ndays_months.get(ee.Number(month).subtract(1))));
    var mo_im = mo_im.clip(study_area);
    return mo_im;
  }
  var ann_im = ee.ImageCollection(order_months.map(month_fn)).sum();
  return ann_im;
}

var sdev_im = ee.ImageCollection(win_year_list.map(year_fn))
                           .reduce(ee.Reducer.stdDev());

var visParam = {min:0.0, 
                max:300,
                bands:['pr_stdDev'],
                palette:['blue', 'purple', 'cyan', 'green', 'yellow', 'red']};
                
Map.addLayer(sdev_im, visParam);
