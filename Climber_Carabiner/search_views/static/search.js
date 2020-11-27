// const BASE_URL = "http://localhost:5000";
const BASE_URL = "https://climbing-carabiner.herokuapp.com";

boulder_levels = [ 'V', 'V0',
         'V1',
         'V2',
         'V3',
         'V4',
         'V5',
         'V6',
         'V7',
         'V8',
         'V9']

         sport_levels = ['5.4','5.5',
         '5.6',
         '5.6+',
         '5.7-',
         '5.7',
         '5.7+',
         '5.8-',
         '5.8',
         '5.8+',
         '5.9-',
         '5.9',
         '5.9+',
         '5.10',
         '5.10a',
         '5.10b',
         '5.10c',
         '5.10d',
         '5.11',
         '5.11a',
         '5.11b',
         '5.11c',
         '5.11d',
         '5.12',
         '5.12a',
         '5.12b',
         '5.12c',
         '5.12d',
         '5.13',
         '5.13a',
         '5.13b',
         '5.13c',
         '5.13d',
         '5.14',
         '5.14a',
         '5.14b']
let map;
let markers = [];

document.addEventListener("DOMContentLoaded", function () {
  let s = document.createElement("script");
  document.head.appendChild(s);
  s.addEventListener("load", async () => {
    const res = await axios.get(`${BASE_URL}/location`);
    map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: parseFloat(res.data.user.lat), lng: parseFloat(res.data.user.lon) },
      zoom: 14,
    });
    let myLatlng = map.getCenter();

    const response = await axios.get(`${BASE_URL}/update_map`);

    for (let routeData of response.data.routes) {
      addMarker({
        coords: { lat: parseFloat(routeData.lat), lng: parseFloat(routeData.lon) },
        title: `<h4>${routeData.name}</h4>`,
      });
    }

    map.addListener("dragend", async () => {
      const res = await axios.post(`${BASE_URL}/update_map`, {
        center: map.getCenter()
      });

      for (let routeData of res.data.routes) {
        addMarker({
          coords: { lat: parseFloat(routeData.lat), lng: parseFloat(routeData.lon) },
          title: `<a href="/route/${routeData.id}"><h3>${routeData.name}</h3></a>`,
        });
        addRouteItem(routeData);
      }

    });



    for (let routeData of response.data.routes) {
      addMarker({
        coords: { lat: parseFloat(routeData.lat), lng: parseFloat(routeData.lon) },
        title: `<a href="/route/${routeData.id}"><h3>${routeData.name}</h3></a>`,
      });

      addRouteItem(routeData);
    }
  });

  $("#search").on("submit click", async (evt) => {
      evt.preventDefault();
      setMapOnAll(null);
      markers = [];
      $("#no-results").empty()
      let routeArray = [];
      let userArray = [];
      $("#route-list").empty();
      $("#user-list").empty();
      let q = $("#q").val();
      let option1 = $("#option1").prop("checked")
      let advanced = $("#advanced").prop("checked")
      let route_type = $("#route_type").val()
      let r_distance = $("#route-distance").val()
      let low, high
      if (route_type == "Boulder") {
      low = $("#b-low").val()
      high = $("#b-high").val()
      } else {
      low = $("#s-low").val()
      high = $("#s-high").val()
      }
      let u_distance = $("#user-distance").val()
      res = await axios.post(`${BASE_URL}/search`, {
        'q': q,
        'option1': option1,
        'advanced': advanced,
        'route_type': route_type,
        'r_distance': r_distance,
        'low': low,
        'high': high,
        'u_distance': u_distance
      });
      console.log(res.data)
      if(res.data.routes && res.data.routes.length != 0) {
        map.panTo(new google.maps.LatLng(parseFloat(res.data.routes[0].lat), parseFloat(res.data.routes[0].lon)))
        routeArray = res.data.routes
        for (let routeData of routeArray) {
          addMarker({
            coords: { lat: parseFloat(routeData.lat), lng: parseFloat(routeData.lon) },
            title: `<a href="/route/${routeData.id}"><h3>${routeData.name}</h3></a>`,
          });
    
          addRouteItem(routeData);
        }
      } else if (res.data.users && res.data.users.length != 0) {
        userArray = res.data.users
        for (let userData of userArray) {
          addUserItem(userData);
        }
      } else {
        $("#user-search").after(`<h5 class="text-danger mt-2" id="no-results" >No Results</h5>`)
      }
    });

  maps = getMapsKey()

  async function getMapsKey() {
    maps = await axios.get(`${BASE_URL}/mapskey`);
    s.src = "https://maps.googleapis.com/maps/api/js?key="+ maps.data;
    return maps.data;
  }



  function addRouteItem(routeData) {
    if (routeData.route_type == "Boulder") {
    $routes = $("#route-list")
    .append(`<li id="${routeData.id}" class="list-group-item list-group-item-action">
      <div class="row justify-content-between">
        <div class="col-lg-4 col-md-4">
        <a href="/route/${routeData.id}">${routeData.name}</a>
        </div>
        <div class="col-lg-2 col-md-2">
          <p>${boulder_levels[routeData.difficulty]}</p>
        </div>
        <div class="col-lg-3 col-md-3">
          <p>${routeData.location}</p>
        </div>
        <div class="col-lg-3 col-md-3">
        <button id="send-route" class="btn btn-sm btn-primary mx-1">Send</button>
        <select class="mx-1" name="attempts" id="attempts">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3+">3+</option>
        </select>
        <button id="project-route" class="btn btn-sm btn-danger" >X</button>
        </div>
      </div>
    </li>`);
    } else {
      $routes = $("#route-list")
    .append(`<li id="${routeData.id}" class="list-group-item list-group-item-action">
      <div class="row justify-content-between">
        <div class="col-lg-4 col-md-4">
        <a href="/route/${routeData.id}">${routeData.name}</a>
        </div>
        <div class="col-lg-2 col-md-2">
          <p>${sport_levels[routeData.difficulty]}</p>
        </div>
        <div class="col-lg-3 col-md-3">
          <p>${routeData.location}</p>
        </div>
        <div class="col-lg-3 col-md-3">
        <button id="send-route" class="btn btn-sm btn-primary mx-1">Send</button>
        <select class="mx-1" name="attempts" id="attempts">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3+">3+</option>
        </select>
        <button id="project-route" class="btn btn-sm btn-danger" >X</button>
        </div>
      </div>
    </li>`);
    }
  }

  function addUserItem(userData) {
    $("#user-list")
    .append(`<li id="${userData.id}" class="list-group-item list-group-item-action">
      <div class="row justify-content-between">
        <div class="col-lg-3 col-md-3">
        <a href="/user/view-profile/${userData.id}">${userData.username}</a>
        </div>
        <div class="col-lg-1 col-md-1 p-0">
          <p><b>B: </b> ${boulder_levels[userData.b_skill_level]}</p>
        </div>
        <div class="col-lg-1 col-md-1 p-0">
        <b>TR: </b> ${sport_levels[userData.tr_skill_level]}</p>
        </div>
        <div class="col-lg-1 col-md-1 p-0">
        <b>LD: </b> ${sport_levels[userData.ld_skill_level]}</p>
        </div>
        <div class="col-lg-3 col-md-3">
          <p>${userData.location}</p>
        </div>
      </div>
    </li>`);
  }

  function addMarker(properties) {
    let marker = new google.maps.Marker({
      position: properties.coords,
      map: map,
      title: properties.title,
    });

    //Check for custom icon
    if(properties.iconImage){
      // Set icon image
      //marker.setIcon();
    }
    if(properties.title) {
      let infoWindow = new google.maps.InfoWindow({
        content:properties.title
      });
      marker.addListener('click', function () {
        infoWindow.open(map, marker);
      });
    }
    markers.push(marker)
  }

  function setMapOnAll(map) {
    for (let i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
  }

  $('#option1').on('click', (evt) => {
    evt.preventDefault();
    $("#no-results").empty()
    let option = $(evt.target.closest("#option1"));
    option.prop("checked", true);
    $("#option2").prop("checked", false);
    $('#route-search').show();
    $('#user-search').hide();
    $('#map').show();
    $('#route-list').show();
    $('#user-list').hide();
    $('#q').attr("placeholder", "Search Routes");
    $("hr").show();

  });

  $('#option2').on('click', (evt) => {
    evt.preventDefault();
    $("#no-results").empty()
    let option = $(evt.target.closest("#option2"));
    option.prop("checked", true);
    $("#option1").prop("checked", false);
    $('#user-search').show();
    $('#map').hide();
    $('#route-search').hide();
    $('#route-list').hide();
    $('#user-list').show();
    $('#q').attr("placeholder", "Search Users");
    $("hr").hide();
  });

  $('#route_type').change(function () {
    if ($(this).val() == "Boulder") {
      console.log("There")
      $('#boulder-low').show();
      $('#boulder-high').show();
      $('#sport-low').hide();
      $('#sport-high').hide();
    } else {
      console.log("Here")
      $('#sport-low').show();
      $('#sport-high').show();
      $('#boulder-low').hide();
      $('#boulder-high').hide();
    }
  })
});