// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});

async function updatePieChart(URL) {
	var res = await fetch(URL);
	console.log(res);
	var json = await res.json();
	console.log(json);
	//json = json[1495]['close'];
	// Area Chart Example
	console.log(myLineChart);
	myPieChart.data = {
    labels: ["긍정", "중립", "부정"],
    datasets: [{
      data: [json['positive'], json['neutral'], json['nagative']],
      backgroundColor: ['#4e73df', '#1cc88a', '#f34336'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#ea0000'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  }
	myPieChart.update();
	var ele = document.getElementById("discuss_href");
	ele.href = json['href'];
}

const Sentiment_URL = "http://localhost:9000/stock/api/sentiment";
updatePieChart(Sentiment_URL);