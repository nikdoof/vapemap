
function supports_geolocation() {
    return 'geolocation' in navigator;
}

function init_geolocation() {
    if (supports_geolocation()) {
        navigator.geolocation.getCurrentPosition(handle_geolocation_event)
    }
}

function handle_geolocation_event(position) {
    $('#geolocation a').attr('href', '/stores/search/?lat=' + position.coords.latitude + '&lng=' + position.coords.longitude + '&distance=10');
    $('#geolocation').fadeIn(1000);
}

$(document).ready(function() {init_geolocation();})