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
      }

  });



  for (let routeData of response.data.routes) {
    addMarker({
      coords: { lat: parseFloat(routeData.lat), lng: parseFloat(routeData.lon) },
      title: `<h4>${routeData.name}</h4>`,
    });
  }
});

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

  s.src =
    "https://maps.googleapis.com/maps/api/js?key=";
});
