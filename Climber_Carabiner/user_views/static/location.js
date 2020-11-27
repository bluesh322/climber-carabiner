//const BASE_URL = "http://localhost:5000";
const BASE_URL = "https://climbing-carabiner.herokuapp.com";

document.addEventListener("DOMContentLoaded", async function () {
    $("#location").on("click", function (evt) {
        if(navigator.geolocation){
            const perm = navigator.permissions.query({
                name: 'geolocation'
            }).then(function(result) {
                if (result.state == 'granted') {
                    alert(result.state);
                    geoBtn.style.display = 'none';
                    
                } else if (result.state == 'prompt') {
                    alert(result.state);
                    geoBtn.style.display = 'none';
           
                    navigator.geolocation.getCurrentPosition(revealPosition, positionDenied, geoSettings);
                } else if (result.state == 'denied') {
                    alert(result.state);
                    geoBtn.style.display = 'inline';
                }
                result.onchange = function() {
                    alert(result.state);
                }
                return result;
            });
            if (perm.state == "granted" || perm.state == "prompt") {
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
                $("#location").after("<p class='text-success'>Success</p>")
                setTimeout(() => { window.location.replace(`${BASE_URL}/user-feed`);}, 4000);
            } else {
                $("#location").after("<p class='text-danger'>You have blocked location permission on your browser, please change this setting for your browser</p>")
            }
        } 
        else {
            $("#location").after("<p class='text-danger'>Geolocation not available on this browser</p>")
        }
    })  
});
