
// Scrpt with variables

// For convenience...
Date.prototype.format = function (mask, utc) {
	return dateFormat(this, mask, utc);
};
api_endpoint = "api/funnel?"

Date.prototype.getWeek = function() {
  var onejan = new Date(this.getFullYear(),0,1);
  return Math.ceil((((this - onejan) / 86400000) + onejan.getDay()+1)/7);
}

var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1; //January is 0!
var yyyy = today.getFullYear();
var week = today.getWeek();

if(dd<10) {
    dd='0'+dd
}

if(mm<10) {
    mm='0'+mm
}

today = yyyy + '-' + mm + '-' + dd;
console.log("Today is: " + today);
console.log("Previous week is : " + (week - 1));


var docid = document.getElementById("today_date");
docid.innerHTML = today;


// function to get this week date in the format: "from YYYY-MM-DD to YYYY-MM-DD"
// var this_week_url = "http://www.funnel.space/api/funnel?period="+ yyyy +"-W"+ (week - 1) +"&metricid=calc-ckan-new-orgs"
// d3.json(this_week_url, function(error, json){
// 	if (error) return error;
// 	enddate = json["resources"][0]["period_end_date"];
// 	startdate = json["resources"][0]["period_start_date"];

// 	var docid = document.getElementById("this_week_dates");
// 	docid.innerHTML = startdate + " to " + enddate;
// });


