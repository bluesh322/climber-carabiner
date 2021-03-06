//const BASE_URL = "http://localhost:5000";
const BASE_URL = "https://climbing-carabiner.herokuapp.com";

document.addEventListener("DOMContentLoaded", async function () {
    $("#user-project-btn").on("click", async function (evt) {
        evt.preventDefault();
        $route = $(evt.target.closest("button")).attr("data-route-id")
        const res = await axios.post(`${BASE_URL}/user/add_project_route/${$route}`, {
            'route_id': $route
        });

        console.log(res);

        let $projectBtn = $(evt.target.closest("button"))
        $projectBtn.after($("<button class='btn btn-success disabled btn-sm addedBtn'>Added</button>"))
        $projectBtn.remove();
        setTimeout(() => { $(".addedBtn").remove() }, 1000);
    })

    $("#user-send-btn").on("click", async function (evt) {
        evt.preventDefault();
        $route = $(evt.target.closest("button")).attr("data-route-id")
        $sendBtn = $(evt.target.closest("button"));
        let $attemptsSelect = $sendBtn.next();
        const res = await axios.post(`${BASE_URL}/user/add_sent_route/${$route}`, {
            'route_id': $route, 
            'attempts': $attemptsSelect[0].value
        });

        console.log(res);
        let $projectBtn = $sendBtn.parent().parent().prev().children().children();
        console.log($projectBtn);
        $sendBtn.after($("<button class='btn btn-success disabled btn-sm addedBtn'>Sent</button>"))
        $sendBtn.after($("<p>Sent Route<p>"))
        $sendBtn.remove();
        $projectBtn.remove();
        $attemptsSelect.remove();
        setTimeout(() => { $(".addedBtn").remove() }, 1000);
    });
    $("#feed-connect").on("click", async function (evt) {
        evt.preventDefault();
        $user = $("#feed-connect").attr("data-user-id")
        const res = await axios.post(`${BASE_URL}/user/add_connection/${$user}`, {
            'user_id': $user
        })
    });

    $("#feed-list").on('click', ".thumbs-up", async function (evt) {
        evt.preventDefault();
        const $userId = $(evt.target.closest("span")).attr("data-project-id");
        let res = await axios.post(`${BASE_URL}/user/toggle_like/${$userId}`, {
            'like_id': $userId
        });
        console.log(res.data.msg);

        evt.target.classList.toggle("far");
        evt.target.classList.toggle("fas");
    });

    $("#feed-list").on('click', ".star", async function (evt) {
        evt.preventDefault();
        const $userId = $(evt.target.closest("span")).attr("data-send-id");
        let res = await axios.post(`${BASE_URL}/user/toggle_kudo/${$userId}`, {
            'like_id': $userId
        });
        console.log(res.data.msg);

        evt.target.classList.toggle("far");
        evt.target.classList.toggle("fas");
    });
});