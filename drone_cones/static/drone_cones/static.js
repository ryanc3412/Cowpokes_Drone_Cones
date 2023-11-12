function timer() {
		// Set the countdown duration to 10 minutes (in milliseconds)
	var distance = 1000 * 60 * 10;

	// Update the count down every 1 second
	var x = setInterval(function() {
	  // Time calculations for minutes and seconds
	  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

	  // Output the result in element with id="count"
	  document.getElementById("count").innerHTML = minutes + "m " + seconds + "s";

	  // Decrease the distance by 1 second (1000 milliseconds)
	  distance -= 1000;

	  // If the count down is over, write some text
	  if (distance < 0) {
	    clearInterval(x);
	    document.getElementById("count").innerHTML = "Order Delivered";
	  }
	}, 1000);
}




//possible lat/lon if we wanna do that
const x = document.getElementById("latLon");

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else { 
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
	//enter whatever the id is into this querySelector
    const addressElement = document.querySelector("#address");

    if (addressElement) {
        const apiKey = 'AIzaSyBpj4Qb9-d2AJjcgXKE1WCr1eEsC-DzoWw';
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${apiKey}`;

        fetch(url)
            .then(response => response.json())
            .then(json => {
                if (json.error) {
                    addressElement.textContent = "Error Fetching Location";
                } else {
                    theData = json;
                    const addy = theData.results[0].formatted_address;
                    addressElement.textContent = addy;
                }
            })
            .catch(error => {
                console.error('Error fetching geolocation data:', error);
            });
    } else {
        console.error('Element with ID "address" not found.');
    }
}




