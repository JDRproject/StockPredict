import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import com.mashape.unirest.request.body.RequestBodyEntity;










response = Unirest.GET ("http://api.apistore.co.kr/opinetbasic//Oil/OilPriceAll.jsp",
  headers={"x-waple-authorization": "고객 키"},
  params={
	OutPut:"Json"   }
)