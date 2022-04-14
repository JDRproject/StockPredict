
const URL_API_NEWS = 'http://localhost:9000/stock/api/news?code=5930';
async function updateNews(URL) {
	var res = await fetch(URL);
	console.log(res);
	var json = await res.json();
	console.log(json);

	var title = json['title'];
	var body_url = json['body_url'];
	var img_src = json['img_src'];
	var body_text_list = json['body_text_list'];
	
	var ele = document.getElementById("news_title");
	ele.innerText = title;
	
	ele = document.getElementById("news_img");
	ele.src = img_src;
	
	ele = document.getElementById("new_href");
	ele.href = body_url;

	ele = document.getElementById("news_body");
	var count = 0;
	var txt = " ";
	
    for (var i = 1; count < 100; i++) { 
		txt += json['body_text_list'][i];
		count = txt.length;
    }
	ele.innerText = txt;
	console.log(json['body_text_list'])

}

updateNews(URL_API_NEWS);

const URL_API_EX = 'http://localhost:9000/stock/api/exchange';
async function updateExchange(URL) {
	var res = await fetch(URL);
	console.log(res);
	var json = await res.json();
	console.log(json);

	var date = json['date'];
	var exchange = json['ttb'];
	var interest = json['int_r'];
	console.log (json['int_r']);
	var ele = document.getElementById("interest");
	ele.innerText = json['int_r'][json['int_r'].length-1] + "%/년";
	var ele = document.getElementById("exchange");
	ele.innerText = json['ttb'][json['ttb'].length-1] + "원/달러";
	
	var intdiff = Number(json['int_r'][json['int_r'].length-1]) - Number(json['int_r'][json['int_r'].length-2]);
	//var ele = document.getElementById("exchange_diff");
	//ele.innerText = "전일 대비 " +String(intdiff);

	}
updateExchange(URL_API_EX);