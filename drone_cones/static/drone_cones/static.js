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
            for (var i = 0; i < data.length; i++) {
                if (data[i]['stockAvailable'] > 0) {
                    if (data[i]['type'] == 'Ice Cream') {
                        flavor1List.push(data[i]);
                        flavor2List.push(data[i]);
                    } else if (data[i]['type'] == 'Cone') {
                        coneList.push(data[i]);
                    } else if (data[i]['type'] == 'Topping') {
                        toppingsList.push(data[i]);
                    }
                }
            }
            // Get the "flavors" div
            var flavors1Div = document.getElementById("flavors1");
            var flavors2Div = document.getElementById("flavors2");
            var conesDiv = document.getElementById("cones");
            var toppingsDiv = document.getElementById("toppings");

            // Create a div for each flavor and append it to the "flavors" div
            for (var i = 0; i < flavor1List.length; i++) {
                var flavor1Div = document.createElement("div");
                var flavor2Div = document.createElement("div");
                var cost1Div = document.createElement("div");
                var cost2Div = document.createElement("div");

                flavor1Div.setAttribute("class", "flavor1Display");
                flavor2Div.setAttribute("class", "flavor2Display");
                flavor1Div.setAttribute("onclick", `selectFlavors1(this, event)`);
                flavor2Div.setAttribute("onclick", `selectFlavors2(this, event)`);
                cost1Div.setAttribute("class", "cost1Val");
                cost2Div.setAttribute("class", "cost2Val");

                flavor1Div.textContent = flavor1List[i]['flavor'];
                cost1Div.textContent = "Cost: $" + flavor1List[i]['cost'];
                flavor1Div.appendChild(cost1Div);

                flavor2Div.textContent = flavor2List[i]['flavor'];
                cost2Div.textContent = "Cost: $" + flavor2List[i]['cost'];

                flavor2Div.appendChild(cost2Div);
                flavors1Div.appendChild(flavor1Div);
                flavors2Div.appendChild(flavor2Div);
            }

            for (var i = 0; i < coneList.length; i++) {
                var coneDiv = document.createElement("div");
                var coneCost = document.createElement("div");

                coneDiv.setAttribute("class", "coneDisplay");
                coneDiv.setAttribute("onclick", `selectCone(this, event)`);
                coneCost.setAttribute("class", "coneCost");

                coneDiv.textContent = coneList[i]['flavor'];
                coneCost.textContent = "Cost: $" + coneList[i]['cost'];

                coneDiv.appendChild(coneCost);
                conesDiv.appendChild(coneDiv);
            }

            for (var i = 0; i < toppingsList.length; i++) {
                var toppingDiv = document.createElement("div");
                var toppingCost = document.createElement("div");

                toppingDiv.setAttribute("class", "toppingsDisplay");
                toppingDiv.setAttribute("onclick",
                    `selectToppings(this, event)`);
                toppingCost.setAttribute("class", "toppingCost");

                toppingDiv.textContent = toppingsList[i]['flavor'];
                toppingCost.textContent = "Cost: $" + toppingsList[i]['cost'];

                toppingDiv.appendChild(toppingCost);
                toppingsDiv.appendChild(toppingDiv);
            }
        })
        .catch(error => console.error('Error:', error));

}

var selectedItems = {
    flavor1: "",
    flavor1Cost: 0,
    flavor2: "",
    flavor2Cost: 0,
    cone: "",
    coneCost: 0,
    toppings: {
        first: "",
        firstCost: 0,
        second: "",
        secondCost: 0,
        third: "",
        thirdCost: 0
    },
    totalConeCost: 0
};

function logSelectedItems() {
    console.log(selectedItems);
}

function selectFlavors1(item, event) {
    if (event && event.type == 'click') {
        var flavor1Items = document.querySelectorAll('.flavor1Display');
        var parentTextContent = item.firstChild.textContent.trim();

        var dollarIndex = item.textContent.indexOf('$');
        var elementAfterDollar = item.textContent.slice(dollarIndex + 1).trim();

        if (selectedItems['flavor1'] == parentTextContent) {
            item.style.backgroundColor = '';
            selectedItems.flavor1 = "";
            selectedItems.totalConeCost -= selectedItems.flavor1Cost;
            selectedItems.flavor1Cost = 0;
        } else {
            if (selectedItems.flavor1 == "") {
                selectedItems.flavor1Cost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.flavor1Cost;
            } else {
                selectedItems.totalConeCost -= selectedItems.flavor1Cost;
                selectedItems.flavor1Cost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.flavor1Cost;
            }
            selectedItems.flavor1 = parentTextContent;
            item.style.backgroundColor = "#008080";
        }

        flavor1Items.forEach(function (el) {
            var elParentTextContent = el.firstChild.textContent.trim();
            if (selectedItems['flavor1'] != elParentTextContent) {
                el.style.backgroundColor = '';  // Reset background color to default (empty string)
            }
        });
    }
}
function selectFlavors2(item, event) {
    if (event && event.type == 'click') {
        var flavor2Items = document.querySelectorAll('.flavor2Display');
        var parentTextContent = item.firstChild.textContent.trim();

        var dollarIndex = item.textContent.indexOf('$');
        var elementAfterDollar = item.textContent.slice(dollarIndex + 1).trim();

        if (selectedItems['flavor2'] == parentTextContent) {
            item.style.backgroundColor = '';
            selectedItems.flavor2 = "";
            selectedItems.totalConeCost -= selectedItems.flavor2Cost;
            selectedItems.flavor2Cost = 0;
        } else {
            if (selectedItems.flavor2 == "") {
                selectedItems.flavor2Cost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.flavor2Cost;
            } else {
                selectedItems.totalConeCost -= selectedItems.flavor2Cost;
                selectedItems.flavor2Cost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.flavor2Cost;
            }
            selectedItems.flavor2 = parentTextContent;
            item.style.backgroundColor = "#008080";
        }

        flavor2Items.forEach(function (el) {
            var elParentTextContent = el.firstChild.textContent.trim();
            if (selectedItems['flavor2'] != elParentTextContent) {
                el.style.backgroundColor = '';  // Reset background color to default (empty string)
            }
        });
    }
}
function selectCone(item, event) {
    if (event && event.type == 'click') {
        var flavorItems = document.querySelectorAll('.coneDisplay');
        var parentTextContent = item.firstChild.textContent.trim();

        var dollarIndex = item.textContent.indexOf('$');
        var elementAfterDollar = item.textContent.slice(dollarIndex + 1).trim();

        if (selectedItems['cone'] == parentTextContent) {
            item.style.backgroundColor = '';
            selectedItems.cone = "";
            selectedItems.totalConeCost -= selectedItems.coneCost;
            selectedItems.coneCost = 0;
        } else {
            if (selectedItems.cone == "") {
                selectedItems.coneCost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.coneCost;
            } else {
                selectedItems.totalConeCost -= selectedItems.coneCost;
                selectedItems.coneCost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.coneCost;
            }
            selectedItems.cone = parentTextContent;
            item.style.backgroundColor = "#008080";
        }

        flavorItems.forEach(function (el) {
            var elParentTextContent = el.firstChild.textContent.trim();
            if (selectedItems['cone'] != elParentTextContent) {
                el.style.backgroundColor = '';  // Reset background color to default (empty string)
            }
        });
    }
}
function selectToppings(item, event) {
    if (event && event.type == 'click') {
        var flavorItems = document.querySelectorAll('.toppingsDisplay');
        var parentTextContent = item.firstChild.textContent.trim();

        var dollarIndex = item.textContent.indexOf('$');
        var elementAfterDollar = item.textContent.slice(dollarIndex + 1).trim();

        if (Object.values(selectedItems['toppings']).includes(parentTextContent)) {
            item.style.backgroundColor = '';
            if (parentTextContent == selectedItems.toppings.first) {
                selectedItems.toppings.first = "";
                selectedItems.totalConeCost -= selectedItems.toppings.firstCost;
                selectedItems.toppings.firstCost = 0;
            }
            if (parentTextContent == selectedItems.toppings.second) {
                selectedItems.toppings.second = "";
                selectedItems.totalConeCost -= selectedItems.toppings.secondCost;
                selectedItems.toppings.secondCost = 0;
            }
            if (parentTextContent == selectedItems.toppings.third) {
                selectedItems.toppings.third = "";
                selectedItems.totalConeCost -= selectedItems.toppings.thirdCost;
                selectedItems.toppings.thirdCost = 0;
            }
        } else if (selectedItems.toppings.first == "") {
            if (selectedItems.toppings.first == "") {
                selectedItems.toppings.firstCost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.toppings.firstCost;
            } else {
                selectedItems.totalConeCost -= selectedItems.toppings.firstCost;
                selectedItems.toppings.firstCost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.toppings.firstCost;
            }
            selectedItems.toppings.first = parentTextContent;
            item.style.backgroundColor = "#008080";
        } else if (selectedItems.toppings.second == "") {
            if (selectedItems.toppings.second == "") {
                selectedItems.toppings.secondCost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.toppings.secondCost;
            } else {
                selectedItems.totalConeCost -= selectedItems.toppings.secondCost;
                selectedItems.toppings.secondCost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.toppings.secondCost;
            }
            selectedItems.toppings.second = parentTextContent;
            item.style.backgroundColor = "#008080";
        } else if (selectedItems.toppings.third == "") {
            if (selectedItems.toppings.third == "") {
                selectedItems.toppings.thirdCost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.toppings.thirdCost;
            } else {
                selectedItems.totalConeCost -= selectedItems.toppings.thirdCost;
                selectedItems.toppings.thirdCost = parseInt(elementAfterDollar);
                selectedItems.totalConeCost += selectedItems.toppings.thirdCost;
            }
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
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
});

function removeItemFromOrder(itemId) {
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
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
}

