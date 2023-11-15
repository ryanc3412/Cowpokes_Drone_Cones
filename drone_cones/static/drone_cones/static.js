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

function writeAddress(checkAddress) {
    var addressOne = document.getElementById("address1");
    var addressTwo = document.getElementById("address2");

    // Use checkAddress.checked to check if the checkbox is checked
    addressTwo.value = checkAddress.checked ? addressOne.value : "";
}


function populate() {
    const flavorList = [
        "Chocolate",
        "Vanilla",
        "Mint Chocolate Chip",
        "Rocky Road",
        "Cookie Dough"
    ];

    const scoopList = [1, 2, 3];
    const coneList = ["Waffle", "Fudge", "Original"];

    // Get the "flavors" div
    var flavorsDiv = document.getElementById("flavors");
    var scoopsDiv = document.getElementById("scoops");
    var conesDiv = document.getElementById("coneflavors");

    // Create a div for each flavor and append it to the "flavors" div
    for (var i = 0; i < flavorList.length; i++) {
        var flavorDiv = document.createElement("div");
        flavorDiv.setAttribute("class", "flavorDisplay");
        flavorDiv.setAttribute("onclick", `selectFlavors(this, event)`);
        flavorDiv.textContent = flavorList[i];
        flavorsDiv.appendChild(flavorDiv);
    }

    for (var i = 0; i < scoopList.length; i++) {
        var scoopDiv = document.createElement("div");
        scoopDiv.setAttribute("class", "scoopDisplay");
		scoopDiv.setAttribute("onclick", "selectScoops(this, event)");
        scoopDiv.textContent = scoopList[i];
        scoopsDiv.appendChild(scoopDiv);
    }

    for (var i = 0; i < coneList.length; i++) {
        var coneDiv = document.createElement("div");
        coneDiv.setAttribute("class", "coneDisplay");
		coneDiv.setAttribute("onclick", "selectCones(this, event)");
        coneDiv.textContent = coneList[i];
        conesDiv.appendChild(coneDiv);
    }
}

var selectedItems = {
	flavor: "",
	scoop: "",
	cone: "",
}

var completedFunctions = 0;

function logSelectedItems() {
	completedFunctions++;
	
	if( completedFunctions % 3 == 0) {
		console.log(selectedItems);
	}
}

function selectFlavors(item, event) {
    if (event && event.type == 'click') {
        var flavorItems = document.querySelectorAll('.flavorDisplay');
        flavorItems.forEach(function (el) {
            el.style.backgroundColor = '';  // Reset background color to default (empty string)
        });
		item.style.backgroundColor = "#008080";
		selectedItems.flavor = item.textContent;

		logSelectedItems();
    }
}

function sendToDatabase(data) {
    const apiUrl = 'your-api-endpoint';

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        console.log('Data sent to the database:', result);
        // Handle the server response if needed
    })
    .catch(error => {
        console.error('Error sending data to the database:', error);
        // Handle the error
    });
}

function selectScoops(item, event) {
	var scoopItems = document.querySelectorAll('.scoopDisplay');
	scoopItems.forEach(function (el) {
		el.style.backgroundColor = '';
	})
	item.style.backgroundColor = "#008080"
	selectedItems.scoop = item.textContent;

	logSelectedItems();
}

function selectCones(item,event) {
	var coneItems = document.querySelectorAll('.coneDisplay');
	coneItems.forEach(function (el) {
		el.style.backgroundColor = '';
	})
	item.style.backgroundColor = "#008080"
	selectedItems.cone = item.textContent;

	logSelectedItems();
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




