//const BASE_URL = "http://localhost:5000";
const BASE_URL = "https://climbing-carabiner.herokuapp.com";


document.addEventListener("DOMContentLoaded", function () {
    let modal = $("#confirmModal");

    modal.modal()
    modal.on('hidden.bs.modal',  function () {
        window.location = `${BASE_URL}/login`;
    });
});

