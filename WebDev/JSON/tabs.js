function select_tab2() {
    var tab2 = document.getElementById("recommendation_tab2");
    tab2.classList.add("recommendation_tab_active");
    var tab1 = document.getElementById("recommendation_tab1");
    tab1.classList.remove("recommendation_tab_active");
    var tab3 = document.getElementById("recommendation_tab3");
    tab3.classList.remove("recommendation_tab_active");
    var content1 = document.getElementById("recommendation_content1");
    content1.classList.add("recommendation_content_inactive");
    var content2 = document.getElementById("recommendation_content2");
    content2.classList.remove("recommendation_content_inactive");
    var content3 = document.getElementById("recommendation_content3");
    content3.classList.add("recommendation_content_inactive");
}

function select_tab1() {
    var tab2 = document.getElementById("recommendation_tab2");
    tab2.classList.remove("recommendation_tab_active");
    var tab1 = document.getElementById("recommendation_tab1");
    tab1.classList.add("recommendation_tab_active");
    var tab3 = document.getElementById("recommendation_tab3");
    tab3.classList.remove("recommendation_tab_active");
    var content1 = document.getElementById("recommendation_content1");
    content1.classList.remove("recommendation_content_inactive");
    var content2 = document.getElementById("recommendation_content2");
    content2.classList.add("recommendation_content_inactive");
    var content3 = document.getElementById("recommendation_content3");
    content3.classList.add("recommendation_content_inactive");
}

function select_tab3() {
    var tab2 = document.getElementById("recommendation_tab2");
    tab2.classList.remove("recommendation_tab_active");
    var tab1 = document.getElementById("recommendation_tab1");
    tab1.classList.remove("recommendation_tab_active");
    var tab3 = document.getElementById("recommendation_tab3");
    tab3.classList.add("recommendation_tab_active");
    var content1 = document.getElementById("recommendation_content1");
    content1.classList.add("recommendation_content_inactive");
    var content2 = document.getElementById("recommendation_content2");
    content2.classList.add("recommendation_content_inactive");
    var content3 = document.getElementById("recommendation_content3");
    content3.classList.remove("recommendation_content_inactive");
}