import { adventure_points_info } from './adventure_points_data.js';

function reload_points() {
    const buildAdventurePoints = (ap) => {

        const ap_val = document.getElementById('adventure_points_val');
        ap_val.innerHTML = "".concat("You currently have ", ap.points, " Adventure Points!")
    };

    buildAdventurePoints(adventure_points_info);
}

var intervalId = setInterval(reload_points, 1000);