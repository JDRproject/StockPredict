from pandas import DataFrame
from db import DB
import sys
import json
import requests
import re
from bs4 import  BeautifulSoup

key = "d7496f9d38094137922af2f1b0f1d663"
endpoint = "https://2zoproject.cognitiveservices.azure.com/"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example function for detecting sentiment in text
def sentiment_analysis_example(client, documents):

    response = client.analyze_sentiment(documents=documents, language = "ko")[0]
    '''
    print("Document Sentiment: {}".format(response.sentiment))
    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))
    for idx, sentence in enumerate(response.sentences):
        #print("Sentence: {}".format(sentence.text))
        print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
        print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        ))
    '''
    return response

def test_sentiment_analysis_example(client, documents):

    response = client.analyze_sentiment(documents=documents, language = "ko")[0]

    print("Document Sentiment: {}".format(response.sentiment))
    print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))
    for idx, sentence in enumerate(response.sentences):
        print("Sentence: {}".format(sentence.text))
        print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))
        print("Sentence score:\nPositive={0:.2f}\nNeutral={1:.2f}\nNegative={2:.2f}\n".format(
            sentence.confidence_scores.positive,
            sentence.confidence_scores.neutral,
            sentence.confidence_scores.negative,
        ))

    return response
    
def getNews(CODE):
    base_url = "https://finance.naver.com/item/news_news.naver?code={}&page=1&sm=entity_id.basic&clusterId="
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    url = base_url.format(str(CODE).zfill(6))
    req = requests.get(url, headers= headers)
    soup =  BeautifulSoup(req.text, 'html.parser')
    trList = soup.find_all("tr" , {"class":"first"})
    news = trList[0]
    tdList = soup.find_all("td")

    title = str(tdList[0].find("a").contents[0])
    href = str(tdList[0].find("a")["href"])


    body_url = "https://finance.naver.com" + href

    req = requests.get(body_url, headers= headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    body = soup.find("div", {'class':'scr01'})
    body_text = body.find_all(text = True)
    body_text_list = []
    for i in body_text :
        temp = i.text
        if temp == "해당 언론사에서 선정하며 " :
            break
        body_text_list.append(temp)
    img_src = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
    img_src_soup = body.find("img")
    if img_src_soup is not None:
        img_src = str(img_src_soup["src"])
    

    dic = {"title" : title, "body_url" : body_url,
         "body_text_list" : body_text_list, "img_src" : img_src}
    json_val = json.dumps(dic,  ensure_ascii=False)
    print(json_val)
    """
        documents = df['title'].values.tolist()[:100]
    input_document  = ""
    for sentence in documents :
        input_document += sentence+". "
    input_document = [input_document]
    response = sentiment_analysis_example(client, input_document)

    dic = {"sentiment" : response.sentiment, "positive" : response.confidence_scores.positive,
         "neutral" : response.confidence_scores.neutral, "nagative" : response.confidence_scores.negative}
   
    json_val = json.dumps(dic,  ensure_ascii=False)
    print(json_val)
    #print(df.to_json(orient = 'index'))
    """

def getPredictPrice(CODE) :
    db = DB()
    df = db.getTable("predict","where code = {}".format(CODE))
    df.sort_values(by='date', ascending=False)
    df.index = list(range(len(df)))
    temp = df['date'].values.tolist()
    temp2 = df['predict'].values.tolist()

    df = db.getTable("item_10","where code = {}".format(CODE))
    name = df['CONM'][0]
    dic = {"date" : temp, "close" : temp2, "name" : name}

    json_val = json.dumps(dic,  ensure_ascii=False)
    print(json_val)


def main(argv):

    if len(argv) == 3:
        CODE = argv[1]
        FUNC = int(argv[2])
    elif len(argv) == 2:
        CODE = argv[1]
        FUNC = 1
    else:
        return
    if FUNC == 1 :
        getNews(argv[1])
    elif FUNC == 2 :
        getPredictPrice(CODE)

if __name__ == "__main__":
    main(sys.argv)




