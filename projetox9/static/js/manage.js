"use strict"

var markers_location = [];

function init_map() {
    var map = new google.maps.Map(document.getElementById('map'), {
            disableDefaultUI: true,
            zoomControl: true,
            center: {lat: -22.852645, lng: -43.229663},
                zoom: 14
            }),
            markers = [];
        
    for (var i=0; i<markers_location.length;++i) {
        markers.push(new google.maps.Marker({
            icon: 'static/img/blue-dot.png',
            map: map,
        }))
        var LatLng = new google.maps.LatLng(Number(markers_location[i][0]), Number(markers_location[i][1]))
        markers[i].setPosition(LatLng);
        markers[i].setVisible(true);
    }
}
