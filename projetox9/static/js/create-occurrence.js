// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
function init_map() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -22.852645, lng: -43.229663},
        zoom: 14
    });
    var input = /** @type {!HTMLInputElement} */(
        document.getElementById('location-input'));


    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.setTypes([]);
    autocomplete.bindTo('bounds', map);

    var infowindow = new google.maps.InfoWindow();
    var marker = new google.maps.Marker({
        map: map,
        anchorPoint: new google.maps.Point(0, -29)
    });

    autocomplete.addListener('place_changed', function() {
        infowindow.close();
        marker.setVisible(false);
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            //window.alert("No details available for input: '" + place.name + "'");
            return;
        }

        map.setCenter(place.geometry.location);
        map.setZoom(17);  // Why 17? Because it looks good.

        marker.setIcon(/** @type {google.maps.Icon} */({
            url: place.icon,
            size: new google.maps.Size(50, 50),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(17, 34),
            scaledSize: new google.maps.Size(35, 35)
        }));
        marker.setPosition(place.geometry.location);
        document.getElementById("lat").value = place.geometry.lat;
        document.getElementById("lng").value = place.geometry.lng;
        document.getElementById("place_name").value = place.name;
        marker.setVisible(true);

        console.log(place.address_components);
        if (place.address_components) {
            document.getElementById("lat").value = place.address_components[0];
        }
    });
}

document.addEventListener("DOMContentLoaded", function(ev) {
    flatpickr(".flatpickr", {
        enableTime: true,
        altInput: true,
        altFormat: "d/m/Y H:m",
        allowInput: true,
        defaultDate: new Date(),
        time_24hr: true
    });

    document.getElementsByTagName("form")[0].addEventListener('keypress', function(ev){
        if (ev.target.name == "location" && ev.which === 13)
            ev.preventDefault();
    });
});
