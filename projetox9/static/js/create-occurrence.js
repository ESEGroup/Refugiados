"use strict"

/* Remove error GET data */
var query = window.location.search.replace(/^\?/g,"").split("&");
for (var i in query)
    if (query[i].split("=")[0] === "error")
        window.history.replaceState({}, '', window.location.href.replace(query[i],"").replace(/\&$/g,"").replace(/\?$/g,""));

function init_map() {
    var map = new google.maps.Map(document.getElementById('map'), {
            disableDefaultUI: true,
            zoomControl: true,
            center: {lat: -22.852645, lng: -43.229663},
            zoom: 14
        }),
        input = (document.getElementById('location-input')),
        autocomplete = new google.maps.places.Autocomplete(input),
        marker = new google.maps.Marker({
            icon: 'static/img/blue-dot.png',
            map: map,
        }),
        geocoder = new google.maps.Geocoder(),
    autocomplete.bindTo('bounds', map);

    google.maps.event.addListener(map, 'click', function(ev) {
        set_marker(marker, map, ev.latLng);
        geocoder.geocode({'location':ev.latLng}, function(result, status) {
            if (status === 'OK' && result) {
                document.getElementById("place_name").value = result[0].address_components[1].short_name + ", " + result[0].address_components[0].short_name;
                document.getElementById("location-input").value = result[0].formatted_address;
            }
        });
    });

    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.geometry) return;
        set_marker(marker, map, place.geometry.location);

        document.getElementById("place_name").value = place.name;
    });
}

document.addEventListener("DOMContentLoaded", function(ev) {
    flatpickr(".flatpickr", {
        enableTime: true,
        dateFormat: "d/m/Y H:i",
        allowInput: true,
        defaultDate: new Date(),
        time_24hr: true
    });

    document.getElementById("register").addEventListener('keypress', function(ev){
        if (ev.target.name == "location" && ev.which === 13)
            ev.preventDefault();
    });

    document.getElementById("register").addEventListener('submit', function(ev) {
        var error = false;
        if (!is_CPF_valid(this.getElementsByClassName("CPF")[0].value)) {
            this.getElementsByClassName("CPF")[0].parentNode.getElementsByTagName("div")[0].className = "error";
            error = true;
        }

        var list = ["occurrence", "date", "location-input", "lat", "lng", "place_name"];
        for (var i in list) {
            if (document.getElementById(list[i]).value === "") {
                document.getElementById(list[i]).parentNode.getElementsByTagName("div")[0].className = "error";
                error = true
            }
        }

        if (error)
            ev.preventDefault();
    });

    var CPFs = document.getElementsByClassName("CPF");
    for (var i=0; i<CPFs.length;++i){
        CPFs[i].addEventListener('input', function(ev) {
            ev.target.value = format_CPF(ev.target.value);
        });
    }

});

function set_marker(marker, map, location) {
    marker.setVisible(false);

    document.getElementById("lat").value = location.lat();
    document.getElementById("lng").value = location.lng();

    map.setCenter(location);
    map.setZoom(17);

    marker.setPosition(location);
    marker.setVisible(true);
}
