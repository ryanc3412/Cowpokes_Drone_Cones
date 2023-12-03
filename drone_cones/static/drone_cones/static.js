function timer() {
    // Set the countdown duration to 10 minutes (in milliseconds)
    var distance = 1000 * 60 * 10;

    // Update the count down every 1 second
    var x = setInterval(function () {
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
    var flavor1List = [];
    var flavor2List = [];
    var coneList = [];
    var toppingsList = [];

    fetch('/dronecones/get_products/')
        .then(response => response.json())
        .then(data => {
            console.log(data); // handle the data as needed
            for (var i = 0; i < data.length; i++) {
                if (data[i]['type'] == 'Ice Cream') {
                    flavor1List.push(data[i]);
                    flavor2List.push(data[i]);
                } else if (data[i]['type'] == 'Cone') {
                    coneList.push(data[i]);
                } else if (data[i]['type'] == 'Topping') {
                    toppingsList.push(data[i]);
                }
            }
            console.log(flavor1List);
            console.log(coneList);
            console.log(toppingsList);
            // Get the "flavors" div
            var flavors1Div = document.getElementById("flavors1");
            var flavors2Div = document.getElementById("flavors2");
            var conesDiv = document.getElementById("cones");
            var toppingsDiv = document.getElementById("toppings");

            // Create a div for each flavor and append it to the "flavors" div
            for (var i = 0; i < flavor1List.length; i++) {
                var flavor1Div = document.createElement("div");
                var flavor2Div = document.createElement("div");
                flavor1Div.setAttribute("class", "flavor1Display");
                flavor2Div.setAttribute("class", "flavor2Display");
                flavor1Div.setAttribute("onclick", `selectFlavors1(this, event)`);
                flavor2Div.setAttribute("onclick", `selectFlavors2(this, event)`);
                flavor1Div.textContent = flavor1List[i]['flavor'];
                flavor2Div.textContent = flavor2List[i]['flavor'];
                flavors1Div.appendChild(flavor1Div);
                flavors2Div.appendChild(flavor2Div);
            }

            for (var i = 0; i < coneList.length; i++) {
                var coneDiv = document.createElement("div");
                coneDiv.setAttribute("class", "coneDisplay");
                coneDiv.setAttribute("onclick", `selectCone(this, event)`);
                coneDiv.textContent = coneList[i]['flavor'];
                conesDiv.appendChild(coneDiv);
            }

            for (var i = 0; i < toppingsList.length; i++) {
                var toppingDiv = document.createElement("div");
                toppingDiv.setAttribute("class", "toppingsDisplay");
                toppingDiv.setAttribute("onclick",
                    `selectToppings(this, event)`);
                toppingDiv.textContent = toppingsList[i]['flavor'];
                toppingsDiv.appendChild(toppingDiv);
            }
        })
        .catch(error => console.error('Error:', error));

}

var cart = [];

var selectedItems = {
    flavor1: "",
    flavor2: "",
    cone: "",
    toppings: {
        first: "",
        second: "",
        third: ""
    }
};

var completedFunctions = 0;

function logSelectedItems() {
    completedFunctions++;

    console.log(selectedItems);
}

function selectFlavors1(item, event) {
    if (event && event.type == 'click') {
        var flavor1Items = document.querySelectorAll('.flavor1Display');

        if (selectedItems['flavor1'] == item.textContent) {
            item.style.backgroundColor = '';
            selectedItems.flavor1 = "";
        } else {
            selectedItems.flavor1 = item.textContent;
            document.getElementById('items').value = selectedItems.flavor1;
            item.style.backgroundColor = "#008080";
        }

        flavor1Items.forEach(function (el) {
            if (selectedItems['flavor1'] != el.textContent) {
                el.style.backgroundColor = '';  // Reset background color to default (empty string)
            }
        });

        logSelectedItems();
    }
}
function selectFlavors2(item, event) {
    if (event && event.type == 'click') {
        var flavor2Items = document.querySelectorAll('.flavor2Display');

        if (selectedItems['flavor2'] == item.textContent) {
            item.style.backgroundColor = '';
            selectedItems.flavor2 = "";
        } else {
            selectedItems.flavor2 = item.textContent;
            item.style.backgroundColor = "#008080";
            document.getElementById('items').value = selectedItems.flavor2;
        }

        flavor2Items.forEach(function (el) {
            if (selectedItems['flavor2'] != el.textContent) {
                el.style.backgroundColor = '';  // Reset background color to default (empty string)
            }
        });

        logSelectedItems();
    }
}
function selectCone(item, event) {
    if (event && event.type == 'click') {
        var flavorItems = document.querySelectorAll('.coneDisplay');

        if (selectedItems['cone'] == item.textContent) {
            item.style.backgroundColor = '';
            selectedItems.cone = "";
        } else {
            selectedItems.cone = item.textContent;
            item.style.backgroundColor = "#008080";
            document.getElementById('items').value = selectedItems.cone;
        }

        flavorItems.forEach(function (el) {
            if (selectedItems['cone'] != el.textContent) {
                el.style.backgroundColor = '';  // Reset background color to default (empty string)
            }
        });

        logSelectedItems();
    }
}
function selectToppings(item, event) {
    if (event && event.type == 'click') {
        var flavorItems = document.querySelectorAll('.toppingsDisplay');

        if (Object.values(selectedItems['toppings']).includes(item.textContent)) {
            item.style.backgroundColor = '';
            if (item.textContent == selectedItems.toppings.first) {
                selectedItems.toppings.first = "";
            }
            if (item.textContent == selectedItems.toppings.second) {
                selectedItems.toppings.second = "";
            }
            if (item.textContent == selectedItems.toppings.third) {
                selectedItems.toppings.third = "";
            }
        } else if (selectedItems.toppings.first == "") {
            selectedItems.toppings.first = item.textContent;
            document.getElementById('items').value = selectedItems.toppings.first;
            item.style.backgroundColor = "#008080";
        } else if (selectedItems.toppings.second == "") {
            selectedItems.toppings.second = item.textContent;
            document.getElementById('items').value = selectedItems.toppings.second;
            item.style.backgroundColor = "#008080";
        } else if (selectedItems.toppings.third == "") {
            selectedItems.toppings.third = item.textContent;
            document.getElementById('items').value = selectedItems.toppings.third;
            item.style.backgroundColor = "#008080";
        } else {
            console.log("Sorry, topping cart is full");
        }

        flavorItems.forEach(function (el) {
            if (!Object.values(selectedItems).includes(el.textContent)) {
                el.backgroundColor = '';  // Reset background color to default (empty string)
            }
        });


        logSelectedItems();
    }
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

function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(`${name}=`))
        ?.split('=')[1];

    return cookieValue ? decodeURIComponent(cookieValue) : null;
}

const csrftoken = getCookie('csrftoken');

document.getElementById('addToCart').addEventListener('click', function () {
    fetch('/dronecones/add_to_cart/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(selectedItems),
    })
        .then(response => {
            if (response.headers.get('X-Redirect')) {
                window.location.href = response.headers.get('X-Redirect');
            } else {
                return response.json();
            }
        })
        .then(data => {
            console.log('Success:', data);
            console.log(data);

        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
});


