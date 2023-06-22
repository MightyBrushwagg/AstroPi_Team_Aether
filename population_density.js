
// Input coordinates
var longitude = prompt("Enter longitude");
var latitude = prompt("Enter latitude");
var longitude = parseFloat(longitude);
var latitude = parseFloat(latitude);


// Create a point geometry using the coordinates
var point = ee.Geometry.Point([longitude, latitude]);

// Set the buffer length in meters
var bufferLength = 300000;

// Create a buffer around the point with the specified length
var buffer = point.buffer(bufferLength);

// Visualize the buffer on the map
Map.addLayer(buffer, {color: 'red'}, 'Buffer Area');
var dataset = ee.ImageCollection('CIESIN/GPWv411/GPW_Population_Density')
                  .filterDate('2000-01-01', '2020-12-31');

function calculatePopulationDensity(year) {
  var yearImage = dataset.filterDate(year + '-01-01', year + '-12-31').first();
  var raster = yearImage.select('population_density');
  
  var populationDensity = raster.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: buffer,
    scale: 1000,
    maxPixels: 1e9
  });
  
  return populationDensity.get('population_density');
}



var years = [2000, 2005, 2010, 2015, 2020];
// Calculate population density for every 5 years
years.forEach(function(year) {
  var density = calculatePopulationDensity(year);
  print('Population Density for ' + year + ':', density);
});

// Set the zoom level for the map 
var zoomLevel = 10;
// Center the map on the given coordinates and zoom level
Map.setCenter(longitude, latitude, zoomLevel);
