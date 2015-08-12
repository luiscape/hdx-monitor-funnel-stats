// current_week.js

function SetWeek(div_id) {
  var docid = document.getElementById(div_id);
  docid.innerHTML = (week - 1);
}

SetWeek("current-week");