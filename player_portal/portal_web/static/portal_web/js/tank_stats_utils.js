<!--WN8 Chart-->

const values = JSON.parse(document.getElementById('chart-data').textContent);

new Chart("wn8LineChart", {
  type: "scatter",
  data: {
    datasets: [{
        backgroundColor:"rgba(0,0,255,1.0)",
        borderColor: "rgba(0,0,255,0.1)",
        data: values,
        showLine: true,
        fill: false,
        tension: 0.3
    }]
  },
  options:{
      legend: {display: false},
      title: {
        display: true,
        text: "WN8"
      }
  }
});