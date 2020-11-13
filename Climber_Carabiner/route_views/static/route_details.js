const BASE_URL = "http://localhost:5000";

document.addEventListener("DOMContentLoaded", async function () {
    $("#user-project-btn").on("click", async function (evt) {
        evt.preventDefault();
        $route = $("#user-project-btn").attr("data-route-id")
        const res = await axios.post(`${BASE_URL}user/add_project_route/${$route}`, {
            'route_id': $route
        });

        console.log(res);
    })

    $("#user-send-btn").on("click", async function (evt) {
        evt.preventDefault();
        $route = $("#user-send-btn").attr("data-route-id")
        const res = await axios.post(`${BASE_URL}/user/add_sent_route/${$route}`, {
            'route_id': $route
        });

        console.log(res);
    });
    $("#feed-connect").on("click", async function (evt) {
        evt.preventDefault();
        $user = $("#feed-connect").attr("data-user-id")
        const res = await axios.post(`${BASE_URL}/user/add_connection/${$user}`, {
            'user_id': $user
        })
    });
});