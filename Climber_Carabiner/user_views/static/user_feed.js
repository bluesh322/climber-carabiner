// const BASE_URL = "http://localhost:5000";
const BASE_URL = "https://climbing-carabiner.herokuapp.com";

document.addEventListener("DOMContentLoaded", async function () {

    // const is_location = await axios.get(`${BASE_URL}/user/location`);
    // console.log(is_location.data.res.location)
    // if(is_location.data.res.location) {
    if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(async function (position) {
        console.log(position);
        const res = await axios.get(`${BASE_URL}/mapskey`);
        $.get( "https://maps.googleapis.com/maps/api/geocode/json?latlng="+ position.coords.latitude + "," + position.coords.longitude +"&sensor=false"+`&key=${res.data}`, async function(data) {
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
    // }

    $('#feed-list').on('click', "#project-route", async function (evt) {
        evt.preventDefault();
        let $route = $(evt.target.closest("button")).attr("data-route-id")
        const res = await axios.post(`${BASE_URL}/user/add_project_route/${$route}`, {
            'route_id': $route
        });
        console.log(res)
        let $projectBtn = $(evt.target.closest("button"))
        let $sendBtn = $projectBtn.next();
        let $attemptsSelect = $sendBtn.next();
        $projectBtn.after($("<button class='btn btn-success disabled btn-sm addedBtn'>Added</button>"))
        console.log($($sendBtn))
        $projectBtn.remove();
        setTimeout(() => { $(".addedBtn").remove()}, 1000);
    });

    $('#feed-list').on('click', "#send-route", async function (evt) {
        evt.preventDefault();
        let $route = $(evt.target.closest("button")).attr("data-route-id")
        let $sendBtn = $(evt.target.closest("button"))
        let $attemptsSelect = $sendBtn.next();
        console.log($attemptsSelect[0].value)
        const res = await axios.post(`${BASE_URL}/user/add_sent_route/${$route}`, {
            'route_id': $route,
            'attempts': $attemptsSelect[0].value
        });
        console.log(res)
        let $projectBtn = $sendBtn.prev();
        $sendBtn.after($("<button class='btn btn-success disabled btn-sm addedBtn'>Sent</button>"))
        $sendBtn.remove();
        $projectBtn.remove();
        $attemptsSelect.remove();
        setTimeout(() => { $(".addedBtn").remove() }, 1000);
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
        $connectBtn.after($("<button class='btn btn-success disabled btn-sm addedBtn'>Connected</button>"))
        $connectBtn.remove();
        setTimeout(() => { $(".addedBtn").remove() }, 1000);
    })

    $("#feed-list").on('click', ".thumbs-up", async function (evt) {
        evt.preventDefault();
        const $userId = $(evt.target.closest("span")).attr("data-user-id");
        let res = await axios.post(`${BASE_URL}/user/toggle_like/${$userId}`, {
            'like_id': $userId
        });
        console.log(res.data.msg);

        evt.target.classList.toggle("far");
        evt.target.classList.toggle("fas");
    });

    $("#feed-list").on('click', ".star", async function (evt) {
        evt.preventDefault();
        const $userId = $(evt.target.closest("span")).attr("data-user-id");
        let res = await axios.post(`${BASE_URL}/user/toggle_kudo/${$userId}`, {
            'like_id': $userId
        });
        console.log(res.data.msg);

        evt.target.classList.toggle("far");
        evt.target.classList.toggle("fas");
    });
    
});
