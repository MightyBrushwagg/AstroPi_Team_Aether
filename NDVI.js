// Input longitude and latitude coordinates
var longitude = prompt("Enter longitude");
var latitude = prompt("Enter latitude");
var longitude = parseFloat(longitude);
var latitude = parseFloat(latitude);


// Create a point geometry using the coordinates
var point = ee.Geometry.Point([longitude, latitude]);

// Set the buffer length in meters
var bufferLength = 300000;

// Create a buffer around the point with the specified length
var geometry = point.buffer(bufferLength);

// Import landsat 8 TOA images as it contains red and NIR bands to calculate NDVI from
var landsat = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA');

var years = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021];
years.forEach(function(year) {
  // Get image in specified date and extract median values
  var image = ee.Image(
    landsat.filterBounds(geometry)
    .filterDate(year + '-04-01', year + '-4-28')
    .median()
    );
  //Compute NDVI
  var nir = image.select('B5');
  var red = image.select('B4');
  var ndvi = nir.subtract(red).divide(nir.add(red));
  var ndvi = ndvi.clip(geometry);
  // Define colour paletter for NDVI
  var fastiePalette = [
  '00007F', '0000FF', '0074FF', '00EBFF', '13FF00', 'FFFF00', 'FF7F00', 'FF0000', '800000'];
  //Add map layers
  Map.addLayer(nir, null,"NIR " + year, false)
  Map.addLayer(ndvi, {min:-1, max:1, palette: fastiePalette}, 'continuous NDVI ' + year, false);
  // Filter out all NDVI values < 0.15 (clouds and oceans)
  var ndviFiltered = ndvi.updateMask(ndvi.gt(0.15));
  Map.addLayer(ndviFiltered, {min: -1, max: 1, palette: fastiePalette}, 'Continuous and filtered NDVI ' + year,false);
  // Calculate the mean NDVI of the filtered image using reduceRegion()
  var meanFilteredNdvi = ndviFiltered.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: geometry,
    scale: 1000
  });
  
  // Print the result
  print(year,'mean NDVI', meanFilteredNdvi);
});

// Add map title
var mapTitle = ui.Panel({
  style: {
    position: 'top-center',
    padding: '8px 15px'
  }
});
var mapTitle2 = ui.Label({
  value: 'Map of NDVI',
  style: {
    fontWeight: 'bold',
    fontSize: '20px',
    margin: '0 0 3px 0',
    padding: '0'
    }
});
mapTitle.add(mapTitle2);
Map.add(mapTitle);

// Set the zoom level for the map (higher value means closer zoom)
var zoomLevel = 10;
// Center map
Map.setCenter(longitude, latitude, zoomLevel);
