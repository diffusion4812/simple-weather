// Initialize and add the map
let map;

const stations={
    "SILJ": {lat: 50.211441, lng: -5.480760},
    "CQPY": {lat: 50.170219, lng: -5.100670},
    "ZVDB": {lat: 50.124903, lng: -5.680301},
    "TLFO": {lat: 50.2633173, lng: -5.0518107},
    "URNJ": {lat: 50.233989, lng: -5.2276468},
};

async function initMap() {
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  const position = { lat: 50.4440481, lng: -5.6159588 };

  // The map, centered at Uluru
  map = new Map(document.getElementById("map"), {
    zoom: 8,
    disableDefaultUI: true,
    center: position,
    mapId: "26f1fd542349271f",
  });

  for (let station in stations) {
    const stationTag = document.createElement("div");
    stationTag.className = "station-tag";
    stationTag.textContent = station;

    const marker = new AdvancedMarkerElement({
      map: map,
      position: stations[station],
      content: stationTag,
    });
  }
}

window.initMap = initMap;