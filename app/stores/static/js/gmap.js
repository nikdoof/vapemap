
var store_icon = static_url + 'img/map_icons/home-2.png'
var online_icon = static_url + 'img/map_icons/wifi.png'
var geolocation_icon = static_url + 'img/map_icons/home-2-green.png'

function lookup_marker(id) {
    if (id == null || id == 1) {
        return store_icon
    } else if (id == 2) {
        return online_icon
    } else if (id == 999) {
        return geolocation_icon
    }  else {
        return store_icon
    }
}

function initialize_map(marker_data, element) {
    var mapOptions = {
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(element, mapOptions);
    var bounds = new google.maps.LatLngBounds();

    var markers = [];
    for (var i = 0; i < marker_data.length; i++) {
        var marker = marker_data[i];
        if (marker[1] != null && marker[2] != null) {
            var latlng = new google.maps.LatLng(marker[1], marker[2]);
            bounds.extend(latlng);
            var marker_obj = new google.maps.Marker({
                position: latlng,
                title: marker[0],
                icon: lookup_marker(marker[3])
            });
            if (marker[4] != '') {
                google.maps.event.addListener(marker_obj, 'click', (function(marker) {
                    return function() {
                        window.location = marker[4];
                    }
                })(marker));
            }
            markers.push(marker_obj)
        }
    }
    if (markers.length >= 100) {
        var markerCluster = new MarkerClusterer(map, markers);
    } else {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(map);
        }
    }
    map.fitBounds(bounds)
}