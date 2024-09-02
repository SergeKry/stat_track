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

// Converting date in a human-readable format
document.addEventListener('DOMContentLoaded', function() {
// Original date string
    const lastUpdateElement = document.getElementById('lastUpdate');
    const dateStr = lastUpdateElement.textContent;

    // Convert to Date object
    const dateObj = new Date(dateStr);

    // Format using Intl.DateTimeFormat
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: false,
    };

    const formattedDate = new Intl.DateTimeFormat('en-US', options).format(dateObj);
    lastUpdateElement.textContent = formattedDate;
});