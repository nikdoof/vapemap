
function get_form_latlng() {
    var addr = $('[id$=address1]').val() + ', ' + $('[id$=city]').val() + ', ' + $('[id$=postcode]').val();
    console.log('Inputted address: ' + addr);
    var gc = new google.maps.Geocoder();
    gc.geocode({'address': addr },update_form_latlng);
    return false
}

function update_form_latlng(res, status) {
    if (status == google.maps.GeocoderStatus.OK) {
        if (res.length > 0) {
            res = res[0];
            console.log('Found location: ' + res.formatted_address);
            $('[id$=geo_latitude]').val(res.geometry.location.lat());
            $('[id$=geo_longitude]').val(res.geometry.location.lng());
        }
        $('.form').submit();
    } else {
        alert('Unable to lookup the location for the address provided. Please check and resubmit.');
    }
}

$(document).ready(function(){
    if ($('[id$=geo_latitude]') && $('[id$=geo_latitude]').val() == "" ) {
        $('.form').submit(function(){
            get_form_latlng();
        })
    }
});
