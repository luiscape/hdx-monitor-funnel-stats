// grab latest figures
function LatestFigure(metricid, div_id, share, verbose) {
  var url = api_endpoint + 'metricid=' + metricid;
  var docid = document.getElementById(div_id);
  docid.innerHTML = ('<span><img src="static/img/loading.gif"></span>');
  d3.json(url, function(err, json) {
    if (err) {
      return console.warn(err);
      docid.innerHTML = ('<span>' + "Error." + '</span>');
    } else {
      // gets the latest element.
      data = new DataCollection(json["resources"]);
      var latest_figure = data.query().sort('period', true).values()[0]["value"];
      if (verbose) console.log("Datasets data is: ", latest_figure);
      if (share) latest_figure = numeral(latest_figure).format('0.0%').slice(0, - 1) + '<span class="percent">%</span>';
      var docid = document.getElementById(div_id);
      docid.innerHTML = ('<span>' + latest_figure + '</span>');
    };
  });
};

// building parameters to print the latest data.
// LatestFigure("ckan-number-of-users", "users-top-figure");
// LatestFigure("ckan-number-of-orgs", "orgs-top-figure");
LatestFigure("calc-ckan-new-users", "new-users-top-figure");
LatestFigure("calc-ckan-new-orgs", "new-orgs-top-figure");
LatestFigure("calc-number-of-new-datasets", "new-datasets-top-figure");
LatestFigure("calc-conversion-register", "conv-register-top-figure", true);
LatestFigure("calc-conversion-download", "conv-download-top-figure", true);
LatestFigure("calc-conversion-share", "conv-share-top-figure", true);
