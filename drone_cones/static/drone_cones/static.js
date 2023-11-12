function timer() {
		// Set the countdown duration to 10 minutes (in milliseconds)
	var distance = 1000 * 60 * 10;

	// Update the count down every 1 second
	var x = setInterval(function() {
	  // Time calculations for minutes and seconds
	  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
	  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

	  // Output the result in an element with id="demo"
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

	const scoopList = [
		1,
		2,
		3
	]

	const coneList = [
		"Waffle",
		"Fudge",
		"Original"
	]

	// Get the "flavors" div
	var flavorsDiv = document.getElementById("flavors");
	var scoopsDiv = document.getElementById("scoops");
	var conesDiv = document.getElementById("coneflavors");

	// Create a div for each flavor and append it to the "flavors" div
	for (var i = 0; i < flavorList.length; i++) {
		var flavorDiv = document.createElement("div");
		flavorDiv.setAttribute("class", "productDisplay");
		flavorDiv.setAttribute("onclick", "select(this)")
		flavorDiv.textContent = flavorList[i];
		flavorsDiv.appendChild(flavorDiv);
	}

	for (var i = 0; i < scoopList.length; i++){
		var scoopDiv = document.createElement("div");
		scoopDiv.setAttribute("class", "productDisplay");
		scoopDiv.textContent = scoopList[i];
		scoopsDiv.appendChild(scoopDiv);
	}

	for (var i = 0; i < coneList.length; i++){
		var coneDiv = document.createElement("div");
		coneDiv.setAttribute("class", "productDisplay");
		coneDiv.textContent = coneList[i];
		conesDiv.appendChild(coneDiv);
	}
}