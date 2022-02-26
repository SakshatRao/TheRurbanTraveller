var activated = 0;

function buildCaptures() {

    const capture_div = document.getElementById('capture_div');
    const capture_div2 = document.getElementById('capture_div2');

    if(activated == 0) {
        if(Math.floor(Math.random() * 10) < 2) {
            capture_div.style.display = "none";
            capture_div2.style.display = "none";
            activated = 0;
        } else {
            capture_div.style.display = "inline";
            capture_div2.style.display = "inline";
            activated = 10;
        }
    }
    else {
        capture_div.style.display = "none";
        capture_div2.style.display = "none";
        activated = activated - 1;
    }
}

var intervalId = setInterval(buildCaptures, 5000);