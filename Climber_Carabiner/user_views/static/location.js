//const BASE_URL = "http://localhost:5000";
const BASE_URL = "https://climbing-carabiner.herokuapp.com";

document.addEventListener("DOMContentLoaded", function () {
    $("#location").on("click", function (evt) {
        evt.preventDefault()
        if(navigator.geolocation){
            navigator.permissions.query({
                name: 'geolocation'
            }).then( function(result) {
                if (result.state == 'granted') {
                    navigator.geolocation.getCurrentPosition(async function (position) {
                        console.log(position);
                        const res = await axios.get(`${BASE_URL}/mapskey`);
                        $.get( "https://maps.googleapis.com/maps/api/geocode/json?latlng="+ position.coords.latitude + "," + position.coords.longitude +"&sensor=false"+`&key=${res.data}`, async function(data) {
                                const set_location = await axios.post(`${BASE_URL}/user/location`, {
                                    'lat': position.coords.latitude,
                                    'lon': position.coords.longitude,
                                    'location': `${data.results[0].address_components[2].long_name}, ${data.results[0].address_components[4].long_name}`
                                })
                                console.log(set_location.data)
                            });
                    });
                    $("#location").after("<p class='text-success'>Success, redirecting to user-feed in 5 seconds</p>")
                    setTimeout(() => { window.location.replace(`${BASE_URL}/user-feed`);}, 5000);
                } else if (result.state == 'prompt') {
                    alert("Current Permission Settings: " + result.state);
                    navigator.geolocation.getCurrentPosition(async function (position) {});
                    $("#location").after("<p class='text-danger'>You have blocked location permission on your browser, please change this setting for your browser</p>")
                } else if (result.state == 'denied') {
                    alert("Current Permission Settings: " + result.state);
                    $("#location").after("<p class='text-danger'>You have blocked location permission on your browser, please change this setting for your browser</p>")
                }
            });

        } 
        else {
            $("#location").after("<p class='text-danger'>Geolocation not available on this browser</p>")
        }
    }); 
});
