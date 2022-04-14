// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
	// *     example: number_format(1234.56, 2, ',', ' ');
	// *     return: '1 234,56'
	number = (number + '').replace(',', '').replace(' ', '');
	var n = !isFinite(+number) ? 0 : +number,
		prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
		sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
		dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
		s = '',
		toFixedFix = function(n, prec) {
			var k = Math.pow(10, prec);
			return '' + Math.round(n * k) / k;
		};
	// Fix for IE parseFloat(0.55).toFixed(0) = 0;
	s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
	if (s[0].length > 3) {
		s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
	}
	if ((s[1] || '').length < prec) {
		s[1] = s[1] || '';
		s[1] += new Array(prec - s[1].length + 1).join('0');
	}
	return s.join(dec);
}

var ele = document.getElementById("title1");
ele.innerText = "주식 시세 정보를 불러오고 있습니다..";
var ele = document.getElementById("title2");
ele.innerText = "주식 시세 예측 모델을 불러오고 있습니다..";

var global_data;
var global_label;
var global_data_predict;
var global_label_predict;
var ctx = document.getElementById("myAreaChart");
var predict_ctx= document.getElementById("PredictChart");
var myLineChart = new Chart(ctx, {
	type: 'line',
	options: {
		maintainAspectRatio: false,
		layout: {
			padding: {
				left: 10,
				right: 25,
				top: 25,
				bottom: 0
			}
		},
		scales: {
			xAxes: [{
				time: {
					unit: 'date'
				},
				gridLines: {
					display: false,
					drawBorder: false
				},
				ticks: {
					maxTicksLimit: 10
				}
			}],
			yAxes: [{
				ticks: {
					maxTicksLimit: 10,
					padding: 10,
					// Include a dollar sign in the ticks
					callback: function(value, index, values) {
						return number_format(value) + '원';
					}
				},
				gridLines: {
					color: "rgb(234, 236, 244)",
					zeroLineColor: "rgb(234, 236, 244)",
					drawBorder: false,
					borderDash: [2],
					zeroLineBorderDash: [2]
				}
			}],
		},
		legend: {
			display: false
		},
		tooltips: {
			backgroundColor: "rgb(255,255,255)",
			bodyFontColor: "#858796",
			titleMarginBottom: 10,
			titleFontColor: '#6e707e',
			titleFontSize: 14,
			borderColor: '#dddfeb',
			borderWidth: 1,
			xPadding: 15,
			yPadding: 15,
			displayColors: false,
			intersect: false,
			mode: 'index',
			caretPadding: 10,
			callbacks: {
				label: function(tooltipItem, chart) {
					var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
					return datasetLabel + ': ' + number_format(tooltipItem.yLabel) + '원';
				}
			}
		}
	}
});

var predictChart = new Chart(predict_ctx, {
	type: 'line',
	options: {
		maintainAspectRatio: false,
		layout: {
			padding: {
				left: 10,
				right: 25,
				top: 25,
				bottom: 0
			}
		},
		scales: {
			xAxes: [{
				time: {
					unit: 'date'
				},
				gridLines: {
					display: false,
					drawBorder: false
				},
				ticks: {
					maxTicksLimit: 10
				}
			}],
			yAxes: [{
				ticks: {
					maxTicksLimit: 10,
					padding: 10,
					// Include a dollar sign in the ticks
					callback: function(value, index, values) {
						return number_format(value) + '원';
					}
				},
				gridLines: {
					color: "rgb(234, 236, 244)",
					zeroLineColor: "rgb(234, 236, 244)",
					drawBorder: false,
					borderDash: [2],
					zeroLineBorderDash: [2]
				}
			}],
		},
		legend: {
			display: false
		},
		tooltips: {
			backgroundColor: "rgb(255,255,255)",
			bodyFontColor: "#858796",
			titleMarginBottom: 10,
			titleFontColor: '#6e707e',
			titleFontSize: 14,
			borderColor: '#dddfeb',
			borderWidth: 1,
			xPadding: 15,
			yPadding: 15,
			displayColors: false,
			intersect: false,
			mode: 'index',
			caretPadding: 10,
			callbacks: {
				label: function(tooltipItem, chart) {
					var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
					return datasetLabel + ': ' + number_format(tooltipItem.yLabel) + '원';
				}
			}
		}
	}
});
async function updateChart(URL) {
	var res = await fetch(URL);
	//console.log(res);
	var json = await res.json();
	//console.log(json);
	//json = json[1495]['close'];
	// Area Chart Example
	//console.log(myLineChart);
	myLineChart.data = {
		labels: json['date'],
		datasets: [{
			label: "stock close price",
			lineTension: 0.1,
			backgroundColor: "rgba(78, 115, 223, 0.05)",
			borderColor: "rgba(78, 115, 223, 1)",
			pointRadius: 1,
			pointBackgroundColor: "rgba(78, 115, 223, 1)",
			pointBorderColor: "rgba(78, 115, 223, 1)",
			pointHoverRadius: 3,
			pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
			pointHoverBorderColor: "rgba(78, 115, 223, 1)",
			pointHitRadius: 1,
			pointBorderWidth: 2,
			fill: false,
			data: json['close'],
		}]
	};
	
	global_data = json['close'];
	global_label = json['date'];

	myLineChart.update();
	var ele = document.getElementById("title1");
	ele.innerText = json['name'] + " 주가";
	var ele = document.getElementById("cur_stock_name");
	console.log("==========================")
	console.log(ele.innerText)

	ele.innerText = json['name'];
	
	var ele = document.getElementById("current_price");
	var len = json['close'].length - 1;
	var close_price = json['close'][len];
	console.log("==========================")
	
	ele.innerText = close_price.toLocaleString('ko-KR');
	
	return json['close']
}
async function updatePredictChart(URL) {
	var res = await fetch(URL);
	console.log(res);
	var json = await res.json();
	//console.log(json);
	//json = json[1495]['close'];
	// Area Chart Example
	predictChart.data = {
		labels: json['date'],
		datasets: [{
			label: "stock close price",
			lineTension: 0.1,
			backgroundColor: "rgba(255, 115, 223, 0.05)",
			borderColor: "rgba(255, 115, 223, 1)",
			pointRadius: 1,
			pointBackgroundColor: "rgba(255, 115, 223, 1)",
			pointBorderColor: "rgba(255, 115, 223, 1)",
			pointHoverRadius: 3,
			pointHoverBackgroundColor: "rgba(255, 115, 223, 1)",
			pointHoverBorderColor: "rgba(255, 115, 223, 1)",
			pointHitRadius: 1,
			pointBorderWidth: 2,
			fill: false,
			data: json['close'],
		}]
		
	};
	predictChart.update();
	var ele = document.getElementById("title2");
	ele.innerText = json['name'] + " 주가 예측 모델";
	

	var len = json['close'].length - 1;

	
	var predict_rate = ((json['close'][len] / json['close'][len-1]) - 1) *100;
	ret_rate = json['close'][len] / json['close'][len-1];
	predict_rate = predict_rate.toFixed(2);
	console.log(predict_rate + "%");
	var ele = document.getElementById("predict_rate");
	ele.innerText = predict_rate + "%"
	
	global_data_predict = json['close'];
	global_label_predict = json['date'];
		
	
	return ret_rate;
}

const URL_API = 'http://localhost:9000/stock/api/test';
const URL_API2 = 'http://localhost:9000/stock/api/test?code=6400';
const PREDICT_URL = "http://localhost:9000/stock/api/test?code=5930&func=2";

Promise.all([updateChart(URL_API),updatePredictChart(PREDICT_URL)]).then((values) => {
		var len = values[0].length - 1;
		var ele = document.getElementById("predict_price");
		var val = Math.ceil((values[0][len-1]*values[1]) / 100) * 100; 
		ele.innerText = val.toLocaleString('ko-KR');
		var diff = val - values[0][len];
		diffstr = diff.toLocaleString('ko-KR');
		var ele = document.getElementById("predict_recommand");
		if (diff == 0)
			ele.innerText = "예상 일치";
		else if (diff > 0)
			ele.innerText = diffstr + "p 상승 예측";
		else
			ele.innerText = diffstr + "p 하락 예측";
		console.log(diff);});
