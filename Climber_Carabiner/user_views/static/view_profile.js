// const BASE_URL = "http://localhost:5000";
const BASE_URL = "https://climbing-carabiner.herokuapp.com";

document.addEventListener("DOMContentLoaded", async function () {
    const project_res = await axios.get(`${BASE_URL}/user/projects`);
    const send_res = await axios.get(`${BASE_URL}/user/sends`);

    console.log(project_res);

    console.log(send_res);
    
    $("#project-list").on("click", "#project-route", async function (evt) {
        evt.preventDefault();
        let $route = $(evt.target.closest("li")).attr("id");
        const res = await axios.post(`${BASE_URL}/user/add_project_route/${$route}`, {
            'route_id': $route
        });

        console.log(res);

        let $listItem = $(evt.target.closest("li"));
        $listItem.remove();
        
    });

    $("#project-list").on("click", "#send-route", async function (evt) {
        evt.preventDefault();
        let $route = $(evt.target.closest("li"));
        let $sendBtn = $(evt.target.closest("button"))
        let $attemptsSelect = $sendBtn.next();
        const res = await axios.post(`${BASE_URL}/user/add_sent_route/${$route.attr("id")}`, {
            'route_id': $route,
            'attempts': $attemptsSelect[0].value
        });
        let routeName = $route.children("div").children("div").children("a")[0].innerHTML;
        $sendBtn.remove();
        $attemptsSelect.remove();
        console.log(res)

        $('#send-list').append(`<li class="list-group-item list-group-item-action">          <div class="row justify-content-between">
        <div class="col-lg-4 col-md-4">
        <a class="" href="/route/${res.data.sent.route_id}">${routeName}</a>
        </div>
        <div class="col-2">
        <button id="sent-route" data-route-id="${res.data.sent.route_id}" class="btn btn-sm btn-danger">X</button>
        </div>
      </div></li>`)
        $route.remove();
    });

    $("#send-list").on("click", "#sent-route", async function (evt) {
        evt.preventDefault();
        let $send = $(evt.target.closest("button"));
        const res = await axios.post(`${BASE_URL}/user/add_sent_route/${$send.attr("data-route-id")}`, {
            'route_id': $send,
        })
        console.log(res)

        let $listItem = $(evt.target.closest("li"));
        $listItem.remove()
    });

    $("#connection-list").on("click", "#disconnect-button", async function (evt) {
        evt.preventDefault();
        let $user = $(evt.target.closest("button")).attr("data-user-id");
        console.log($user);
        const res = await axios.post(`${BASE_URL}/user/rem_connection/${$user}`, {
            'user_id': $user
        });
        console.log(res);

        let $listItem = $(evt.target.closest("li"));
        $listItem.remove();

    });

    $("#project-list").on('click', ".thumbs-up", async function (evt) {
        evt.preventDefault();
        const $userId = $(evt.target.closest("span")).attr("data-project-id");
        let res = await axios.post(`${BASE_URL}/user/toggle_like/${$userId}`, {
            'like_id': $userId
        });
        console.log(res.data.msg);

        evt.target.classList.toggle("far");
        evt.target.classList.toggle("fas");
    });

    $("#send-list").on('click', ".star", async function (evt) {
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