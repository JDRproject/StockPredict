function updateAll(CODE) {
	console.log(CODE);
	
	var URL_API = 'http://localhost:9000/stock/api/test?code='+CODE;
	console.log(updateChart(URL_API));

	const PREDICT_URL = "http://localhost:9000/stock/api/test?code=" + CODE + "&func=2";
	//console.log(updatePredictChart(PREDICT_URL));
	
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
		
		
	var URL_API_NEWS = 'http://localhost:9000/stock/api/news?code=' + CODE;
	updateNews(URL_API_NEWS);
	
	var SENTIMENT_URL = "http://localhost:9000/stock/api/sentiment?code=" + CODE;
	updatePieChart(SENTIMENT_URL);

}

function setPeriod(PERIOD) {
		var temp = global_data.slice(PERIOD*-1);
		var temp2 = global_label.slice(PERIOD*-1);

		myLineChart.data.labels = temp2;
		myLineChart.data.datasets[0].data = temp;
		myLineChart.update();
}

function setPeriodPredict(PERIOD) {
		var temp = global_data_predict.slice(PERIOD*-1);
		var temp2 = global_label_predict.slice(PERIOD*-1);

		predictChart.data.labels = temp2;
		predictChart.data.datasets[0].data = temp;
		predictChart.update();
}