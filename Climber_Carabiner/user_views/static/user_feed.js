const BASE_URL = "http://localhost:5000";

document.addEventListener("DOMContentLoaded", async function () {

    const is_location = await axios.get(`${BASE_URL}/user/location`);
    console.log(is_location.data.res.location)
    if(is_location.data.res.location) {
        if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(async function (position) {
            console.log(position);
            $.get( "https://maps.googleapis.com/maps/api/geocode/json?latlng="+ position.coords.latitude + "," + position.coords.longitude +"&sensor=false"+`&key=${process.env.MP_KEY}`, async function(data) {
                    console.log(data);
                    console.log(data.results[0].address_components[2].long_name);
                    console.log(data.results[0].address_components[4].long_name);
                    const set_location = await axios.post(`${BASE_URL}/user/location`, {
                        'lat': position.coords.latitude,
                        'lon': position.coords.longitude,
                        'location': `${data.results[0].address_components[2].long_name}, ${data.results[0].address_components[4].long_name}`
                    })
                    console.log(set_location.data)
                });
        });


        } 
        else {
            console.log("Geolocation is not supported")
        }
    }

    $('#feed-list').on('click', "#project-route", async function (evt) {
        evt.preventDefault();
        let $route = $("#project-route").attr("data-route-id")
        const res = await axios.post(`${BASE_URL}/user/add_project_route/${$route}`, {
            'route_id': $route
        });
        console.log(res)

        let $projectBtn = $(evt.target.closest("button"))
        $projectBtn.text("Added");
        $projectBtn.removeClass("btn-primary");
        $projectBtn.addClass("btn-success disabled");
        $(evt.target.closest("li")).off("click", "#project-route");
    });

    $("#sidebar-list").on('click', "#connect-button", async function (evt) {
        evt.preventDefault();
        let $user = $(evt.target.closest("button")).attr("data-user-id");
        console.log($user)
        const res = await axios.post(`${BASE_URL}/user/add_connection/${$user}`, {
            'follow_id': $user
        });

        console.log(res);
    })

    $("#feed-list").on('click', "#connect-button", async function (evt) {
        evt.preventDefault();
        let $user = $(evt.target.closest("button")).attr("data-user-id");
        const res = await axios.post(`${BASE_URL}/user/add_connection/${$user}`, {
            'follow_id': $user
        });

        console.log(res)

        let $connectBtn = $(evt.target.closest("button"));
        $connectBtn.remove();
    })
    
});
