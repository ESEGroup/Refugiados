"use strict"

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
            infowindow = new google.maps.InfoWindow();

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

    document.getElementsByTagName("form")[0].addEventListener('keypress', function(ev){
        if (this.getElementByClassName("CPF")[0].value.length < 14) {
            ev.preventDefault();
        } else if (!(ev.target.name == "location" && ev.which === 13)) {
            ev.preventDefault();
        }
    });

    var CPFs = document.getElementsByClassName("CPF");
    for (var i=0; i<CPFs.length;++i){
        CPFs[i].addEventListener('input', function(ev) {
            var content = ev.target.value.replace(/\./g,"").replace(/-/g,"");
            ev.target.value = format_CPF(content);
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
