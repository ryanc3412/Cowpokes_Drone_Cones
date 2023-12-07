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
    var city = document.getElementById("city");
    var state = document.getElementById("state")
    var zip = document.getElementById("zip")

    if (checkAddress.checked) {
        fetch('/dronecones/get_account_address/')
            .then(response => response.json())
            .then(data => {
                console.log(data)
                addressOne.value = data['address1'];
                addressTwo.value = data['address2'];
                city.value = data['city'];
                state.value = data['state'];
                zip.value = data['zip'];
            })
    }
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
                var flavor1ImageDiv = document.createElement("img");
                var flavor2Div = document.createElement("div");
                var costDiv = document.createElement("div");
                // var iceCreamImagePath = "`{%` static 'drone_cones/images/ice_cream_cone.png' `%}`";

                flavor1Div.setAttribute("class", "flavor1Display");
                flavor2Div.setAttribute("class", "flavor2Display");
                flavor1Div.setAttribute("onclick", `selectFlavors1(this, event)`);
                flavor2Div.setAttribute("onclick", `selectFlavors2(this, event)`);
                costDiv.setAttribute("class", "costVal");
                // flavor1ImageDiv.setAttribute("class", "flavorImage");

                flavor1Div.textContent = flavor1List[i]['flavor'];
                // flavor1ImageDiv.src = iceCreamImagePath;
                costDiv.textContent = "Cost: $" + flavor1List[i]['cost'];
                flavor1Div.appendChild(costDiv);
                // flavor1Div.appendChild(flavor1ImageDiv);
                // flavor1Div.innerHTML = '<img src="' + iceCreamImagePath + '" alt="ice cream image"><br>' + '<br>' + flavor1List[i]['flavor'] + '<br><div>Cost: $' + flavor1List[i]['cost'] + '</div>';
                flavor2Div.innerHTML = flavor2List[i]['flavor'] + '<br>Cost: $' + flavor2List[i]['cost'];

                flavors1Div.appendChild(flavor1Div);
                flavors2Div.appendChild(flavor2Div);
            }

            for (var i = 0; i < coneList.length; i++) {
                var coneDiv = document.createElement("div");
                coneDiv.setAttribute("class", "coneDisplay");
                coneDiv.setAttribute("onclick", `selectCone(this, event)`);
                coneDiv.innerHTML = coneList[i]['flavor'] + '<br>Cost: $' + coneList[i]['cost'];
                conesDiv.appendChild(coneDiv);
            }

            for (var i = 0; i < toppingsList.length; i++) {
                var toppingDiv = document.createElement("div");
                toppingDiv.setAttribute("class", "toppingsDisplay");
                toppingDiv.setAttribute("onclick",
                    `selectToppings(this, event)`);
                toppingDiv.innerHTML = toppingsList[i]['flavor'] + '<br>Cost: $' + toppingsList[i]['cost'];
                toppingsDiv.appendChild(toppingDiv);
            }
        })
        .catch(error => console.error('Error:', error));

}

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

function logSelectedItems() {
    console.log(selectedItems);
}

function selectFlavors1(item, event) {
    if (event && event.type == 'click') {
        var flavor1Items = document.querySelectorAll('.flavor1Display');

        var parentTextContent = item.firstChild.textContent.trim();

        if (selectedItems['flavor1'] == parentTextContent) {
            item.style.backgroundColor = '';
            selectedItems.flavor1 = "";
        } else {
            selectedItems.flavor1 = parentTextContent;
            item.style.backgroundColor = "#008080";
        }

        flavor1Items.forEach(function (el) {
            var elParentTextContent = el.firstChild.textContent.trim();
            if (selectedItems['flavor1'] != elParentTextContent) {
                el.style.backgroundColor = '';  // Reset background color to default (empty string)
            }
        });

        logSelectedItems();
    }
}
function selectFlavors2(item, event) {
    if (event && event.type == 'click') {
        var flavor2Items = document.querySelectorAll('.flavor2Display');

        var parentTextContent = item.firstChild.textContent.trim();

        if (selectedItems['flavor2'] == parentTextContent) {
            item.style.backgroundColor = '';
            selectedItems.flavor2 = "";
        } else {
            selectedItems.flavor2 = parentTextContent;
            item.style.backgroundColor = "#008080";
        }

        flavor2Items.forEach(function (el) {
            var elParentTextContent = el.firstChild.textContent.trim();
            if (selectedItems['flavor2'] != elParentTextContent) {
                el.style.backgroundColor = '';  // Reset background color to default (empty string)
            }
        });

        logSelectedItems();
    }
}
function selectCone(item, event) {
    if (event && event.type == 'click') {
        var flavorItems = document.querySelectorAll('.coneDisplay');

        var parentTextContent = item.firstChild.textContent.trim();

        if (selectedItems['cone'] == parentTextContent) {
            item.style.backgroundColor = '';
            selectedItems.cone = "";
        } else {
            selectedItems.cone = parentTextContent;
            item.style.backgroundColor = "#008080";
        }

        flavorItems.forEach(function (el) {
            var elParentTextContent = el.firstChild.textContent.trim();
            if (selectedItems['cone'] != elParentTextContent) {
                el.style.backgroundColor = '';  // Reset background color to default (empty string)
            }
        });

        logSelectedItems();
    }
}
function selectToppings(item, event) {
    if (event && event.type == 'click') {
        var flavorItems = document.querySelectorAll('.toppingsDisplay');
        var parentTextContent = item.firstChild.textContent.trim();

        if (Object.values(selectedItems['toppings']).includes(parentTextContent)) {
            item.style.backgroundColor = '';
            if (parentTextContent == selectedItems.toppings.first) {
                selectedItems.toppings.first = "";
            }
            if (parentTextContent == selectedItems.toppings.second) {
                selectedItems.toppings.second = "";
            }
            if (parentTextContent == selectedItems.toppings.third) {
                selectedItems.toppings.third = "";
            }
        } else if (selectedItems.toppings.first == "") {
            selectedItems.toppings.first = parentTextContent;
            item.style.backgroundColor = "#008080";
        } else if (selectedItems.toppings.second == "") {
            selectedItems.toppings.second = parentTextContent;
            item.style.backgroundColor = "#008080";
        } else if (selectedItems.toppings.third == "") {
            selectedItems.toppings.third = parentTextContent;
            item.style.backgroundColor = "#008080";
        } else {
            console.log("Sorry, topping cart is full");
        }

        flavorItems.forEach(function (el) {
            var elParentTextContent = el.firstChild.textContent.trim();
            if (!Object.values(selectedItems).includes(elParentTextContent)) {
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
    var selectedItemsCopy;
    if (selectedItems.cone == "") {
        alert("You must at least order a cone if you want your order!")
        selectedItemsCopy = 'Invalid Order';
    } else {
        selectedItemsCopy = selectedItems;
    }
    fetch('/dronecones/add_to_cart/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(selectedItemsCopy),
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

function removeItemFromOrder(itemId) {
    console.log(itemId);
    fetch('/dronecones/remove_from_order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'text/plain',
            'X-CSRFToken': csrftoken,
        },
        body: itemId
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
}

