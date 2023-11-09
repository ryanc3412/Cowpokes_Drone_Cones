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