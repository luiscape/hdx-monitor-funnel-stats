// bargraph.js
// start with the activity graph: https://scraperwiki.com/dataset/7c6jufm

// function to generate time-series
// sparklines using an API endpoint from
// HDX. this function depends on:
// -- c3.js
// -- d3.js
// -- datacollection.js (you can use jsonpath.js instead)
function GenerateSparkline(metricid, div_id, share, mean, regression, verbose) {

  var url = api_endpoint + 'metricid=' + metricid;
  if (verbose) console.log("The URL for the sparkline is:", url);

  d3.json(url, function(error, json) {
    if (error) return console.warn(error);

    // filtering the data
    var data, values, dates, ind_data;
    data = new DataCollection(json["resources"])
      .query()
      .sort('period', false)
      .filter({
        period__gte: '2014-W44'
      })
      .values();

    // var dates = [];
    var values = [];
    var chart_data = [];
    for (i = 0; i < data.length; i++) {
      if (data[i]["period"].length == 8) {
        chart_data.push({
          date: data[i]["period"],
          value: data[i]["value"]
        });
        values.push(data[i]["value"]);
      };
    };

    var mean_data = {};
    if (mean) {
      var mean_value = ss.mean(values);
      mean_data['value'] = ss.mean(values);
      if (share) mean_data['text'] = numeral(mean_data.text).format('0.0%');
      else mean_data['text'] = Math.round(mean_data.text);
    } else mean_data = null;

    if (verbose) console.log(mean_data);
    if (verbose) console.log(JSON.stringify(chart_data));

    c3.generate({
      bindto: div_id,
      data: {
        // x: 'date',
        json: chart_data,
        keys: {
          x: 'date',
          value: ['value']
        },
        type: 'spline',
        labels: false,
        selection: {
          enabled: true,
          grouped: false,
          multiple: false,
        },
      },
      bar: {
        width: {
          ratio: .88
        }
      },
      point: {
        show: true
      },
      legend: {
        show: false
      },
      color: {
        pattern: ["#34495e"]
      },
      size: {
        height: 100
      },
      axis: {
        x: {
          show: false,
          type: 'category'
        },
        y: {
          show: false,
          tick: {
            format: function(value) {
              if (share) return d3.format(",.1%")(value);
              else return value;
            }
          }
        }
      }
      // grid: {
      //   y: {
      //     lines: [ mean_data ]
      //   }
      // }
    });

  });


};

// generating sparklines
// each function calls the api endpoint
// from a resource independently.
// this causes a performance issue,
// but demonstrates how each call can be made independendtly.
// GenerateSparkline("ckan-number-of-users", "#users-chart", false, false);
// GenerateSparkline("ckan-number-of-orgs", "#orgs-chart", false, false);
GenerateSparkline("calc-ckan-new-users", "#new-users-chart", false, false);
GenerateSparkline("calc-ckan-new-orgs", "#new-orgs-chart", false, false);
GenerateSparkline("calc-number-of-new-datasets", "#new-datasets-chart", false, false);
GenerateSparkline("calc-conversion-register", "#conversion-register-chart", true, false);
GenerateSparkline("calc-conversion-download", "#conversion-download-chart", true, false);
GenerateSparkline("calc-conversion-share", "#conversion-share-chart", true, false);
