import { reminder } from './reminder_data.js';

const buildReminders = (rem) => {

    const remind_div = document.getElementById('reminder_div');

    if(rem.remind == 0) {
        remind_div.style.display = "none";
    } else {
        remind_div.style.display = "inline";
        const remind_text = document.getElementById('reminder_text');
        remind_text.innerHTML = "".concat("Ready to go to work at ", rem.time, "?<br>Look at your reminders -")
    }
};

buildReminders(reminder);