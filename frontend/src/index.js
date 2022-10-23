let numberOfTickers = 100;
let myChart = null;
let ticker = "ticker_00";
for (let i = 0; i < numberOfTickers; i++) {
  var option = document.createElement("option");
  num_str = "0" + i;
  option.value = "ticker_" + num_str.slice(-2);
  option.text = "ticker_" + num_str.slice(-2);
  document.getElementById("tickers_select").appendChild(option);
}
document.getElementById("tickers_select").onclick = function () {
  ticker = document.getElementById("tickers_select").value;
};
function getData(callback) {
  let url = "http://0.0.0.0:8000/quote/" + ticker + "?all=true";
  let xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) callback(xhr.responseText);
  };
  xhr.open("GET", url, true);
  xhr.send(null);
  return xhr.responseText;
}
function plot_chart(quote_data) {
  let quote_data_obj = JSON.parse(quote_data);
  let history = quote_data_obj.history;
  const labels = Object.keys(history);
  const prices_obj_list = Object.values(history);
  let prices = [];
  for (let i = 0; i < prices_obj_list.length; i++) {
    prices.push(prices_obj_list[i].close);
  }
  const data = {
    labels: labels,
    datasets: [
      {
        label: ticker,
        backgroundColor: "rgb(255, 99, 132)",
        borderColor: "rgb(255, 99, 132)",
        data: prices,
      },
    ],
  };
  const config = {
    type: "line",
    data: data,
    options: {
      animation: {
        duration: 0,
      },
    },
  };
  if (myChart != null) {
    myChart.destroy();
  }
  myChart = new Chart(document.getElementById("myChart"), config);
}
function update_chart() {
  getData(plot_chart);
}
setInterval(update_chart, 1000);
