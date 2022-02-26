import { fuel } from './fuel_data.js';

const buildFuel = (fuel) => {

    const fuel_div = document.getElementById('fuel_div');

    if(fuel.level > 25) {
        fuel_div.style.display = "none";
    } else {
        fuel_div.style.display = "inline";
        const fuel_text = document.getElementById('fuel_text');
        fuel_text.innerHTML = "".concat("ALERT: Fuel level is low (", fuel.level, "%)")
    }
};

buildFuel(fuel);