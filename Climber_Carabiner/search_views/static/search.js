const BASE_URL = "http://localhost:5000";
let map;
document.addEventListener("DOMContentLoaded", function () {
  let s = document.createElement("script");
  document.head.appendChild(s);
  s.addEventListener("load", async () => {
    map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: 30.2672, lng: -97.7431 },
      zoom: 12,
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
          title: `<h4>${routeData.name}</h4>`,
        });
        addListItem(routeData);
      }

    });



    for (let routeData of response.data.routes) {
      addMarker({
        coords: { lat: parseFloat(routeData.lat), lng: parseFloat(routeData.lon) },
        title: `<a href="/route/${routeData.id}"><h4>${routeData.name}</h4></a>`,
      });

      addListItem(routeData);
    }
  });

  function addListItem(routeData) {
    $routes = $("#route-list")
    .append(`<li id="${routeData.id}" class="list-group-item list-group-item-action">
      <div class="row justify-content-between">
        <div class="col-lg-4 col-md-4">
        <a href="/route/${routeData.id}">${routeData.name}</a>
        </div>
        <div class="col-lg-2 col-md-2">
          <p>${routeData.difficulty}</p>
        </div>
        <div class="col-lg-3 col-md-3">
          <p>${routeData.route_type}</p>
        </div>
        <div class="col-lg-3 col-md-3">
        <button id="send-route" class="btn btn-sm btn-primary">Send</button>
        <select name="attempts" id="attempts">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3+">3+</option>
        </select>
        <button id="project-route" class="btn btn-sm btn-danger">X</button>
      </div>
      </div>
    </li>
    `);
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

  }

  s.src = 'https://maps.googleapis.com/maps/api/js?key=' + 'GOOGLEMAPSKEY';
});
