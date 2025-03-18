// Initialize and add the map
let wx_map;

const stations={
    "SILJ": {lat: 50.211441, lng: -5.480760},
    "CQPY": {lat: 50.170219, lng: -5.100670},
    "ZVDB": {lat: 50.124903, lng: -5.680301},
    "TLFO": {lat: 50.2633173, lng: -5.0518107},
    "URNJ": {lat: 50.233989, lng: -5.2276468},
};

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    const position = { lat: 50.2698476558, lng: -5.007411412 };

    // The map, centered at Uluru
    wx_map = new Map(document.getElementById("map"), {
        zoom: 9,
        disableDefaultUI: true,
        center: position,
        mapId: "26f1fd542349271f",
    });

    wx_map.addListener("center_changed", () => {
        console.log(wx_map.getZoom());
        console.log(wx_map.getCenter().toJSON());
      });

    for (let station in stations) {
        const stationTag = document.createElement("div");
        stationTag.className = "station-tag";
        stationTag.textContent = station;

        const marker = new AdvancedMarkerElement({
            map: wx_map,
            position: stations[station],
            content: stationTag,
        });
    }
}

export function wx_tr_click(stationId) {
    console.log(stationId);
}

initMap();