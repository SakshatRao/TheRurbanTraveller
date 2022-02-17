import { recommendations1, recommendations2, recommendations3 } from './recommendation_data.js';

const buildRecommendations = (category, category_id, rec, id) => {

    document.getElementById(category_id).innerHTML = category;

    const div1 = document.createElement("div");
    div1.classList.add("recommendation_box");
    const div11 = document.createElement("div");
    div11.classList.add("recommendation_text");
    const div11_h2 = document.createElement("h2");
    const div11_div = document.createElement("div");
    div11_div.classList.add("recommendation_details");
    const div11_div_h31 = document.createElement("h3");
    const div11_div_h32 = document.createElement("h3");
    const div11_div_h33 = document.createElement("h3");
    const div11_div_h34 = document.createElement("h3");

    const rec_content = document.getElementById(id);
    rec_content.appendChild(div1);
    div1.append(div11);
    div11.append(div11_h2);
    div11.append(div11_div);
    div11_div.append(div11_div_h31);
    div11_div.append(div11_div_h32);
    div11_div.append(div11_div_h33);
    div11_div.append(div11_div_h34);

    div11_h2.innerHTML = rec.name;
    div11_div_h31.innerHTML = "".concat("Price - Rs. ", rec.price);
    div11_div_h32.innerHTML = "".concat("Rating - ", rec.rating, "/5");
    div11_div_h33.innerHTML = "".concat(rec.location, " (", rec.distance, " km away)");
    div11_div_h34.innerHTML = "".concat("Duration: ", rec.duration, " hrs");
};

recommendations1.activities.forEach(rec => buildRecommendations(recommendations1.category, "recommendation_tab_title1", rec, "recommendation_content1"));
recommendations2.activities.forEach(rec => buildRecommendations(recommendations2.category, "recommendation_tab_title2", rec, "recommendation_content2"));
recommendations3.activities.forEach(rec => buildRecommendations(recommendations3.category, "recommendation_tab_title3", rec, "recommendation_content3"));