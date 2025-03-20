// Global variable to store the map instance
let wx_map;

// Object containing weather station data with station IDs as keys
// Each station has latitude (lat) and longitude (lng) coordinates
const stations = {
    "SILJ": { lat: 50.211441, lng: -5.480760 },
    "CQPY": { lat: 50.170219, lng: -5.100670 },
    "ZVDB": { lat: 50.124903, lng: -5.680301 },
    "TLFO": { lat: 50.2633173, lng: -5.0518107 },
    "URNJ": { lat: 50.233989, lng: -5.2276468 },
};

// Function to initialize the Google Map
async function initMap() {
    // Import the required Google Maps libraries
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

    // Default position to center the map
    const position = { lat: 50.2698476558, lng: -5.007411412 };

    // Create a new map instance and configure its properties
    wx_map = new Map(document.getElementById("map"), {
        zoom: 9, // Initial zoom level
        disableDefaultUI: true, // Disable default map controls
        gestureHandling: "none", // Disable user gestures like zoom and pan
        zoomControl: false, // Disable zoom control buttons
        center: position, // Center the map at the default position
        mapId: "26f1fd542349271f", // Custom map style ID
    });

    // Loop through each station and add a marker to the map
    for (let station in stations) {
        // Create a custom HTML element for the station marker
        const stationTag = document.createElement("div");
        stationTag.className = "station-tag"; // CSS class for styling
        stationTag.textContent = station; // Display the station ID as text

        // Create a new marker and add it to the map
        const marker = new AdvancedMarkerElement({
            map: wx_map, // Attach the marker to the map
            position: stations[station], // Set the marker's position
            content: stationTag, // Use the custom HTML element as the marker's content
        });
    }
}

// Function to handle table row clicks and pan/zoom the map to the selected station
export function wx_tr_click(stationId) {
    // Reset the zoom level before panning
    wx_map.setZoom(9);
    // Pan the map to the selected station's coordinates
    wx_map.panTo(stations[stationId]);
    // Zoom in to focus on the selected station
    wx_map.setZoom(12);
}

// Initialize the map when the script is loaded
initMap();
