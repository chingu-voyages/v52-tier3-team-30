URL = "https://hlpractice.pythonanywhere.com/api"

var API_KEY;
await fetch(URL)
  .then(res => res.json())
  .then(data => {
    API_KEY = data.API;
   });


const autocompleteInput = new autocomplete.GeocoderAutocomplete(
                        document.getElementById("autocomplete"),
                        API_KEY,
                        { /* Geocoder options */ });

var addressInput = document.getElementById("inputAddress")

autocompleteInput.on('select', (location) => {
    // check selected location here
    addressInput.value = autocompleteInput.getValue();
});

autocompleteInput.on('suggestions', (suggestions) => {
    // process suggestions here
});