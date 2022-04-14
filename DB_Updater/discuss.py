from xml.dom.minidom import Document
from numpy import double
import pandas as pd
import requests
import re
from bs4 import  BeautifulSoup

import pymysql
from sqlalchemy import create_engine
import chardet
from sympy import false
from datetime import datetime

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
    return response.sentiment

class Discuss :
    

    base_url = "https://finance.naver.com//item/board.naver?code={}&amp;page=1&page={}"
    def __init__(self) -> None:
        pass

    def update(self, code) :

        code = str(code).zfill(6)

        df = pd.DataFrame()

        for idx in range(10, 0, -1) :
            url = self.base_url.format(code, idx)
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
            req = requests.get(url, headers= headers)
            soup =  BeautifulSoup(req.text, 'html.parser')
            trList = soup.find_all("tr", {"onmouseover":"mouseOver(this)"})

            for tr in trList :
                tdList = tr.find_all('td')
                tdList[0] = tdList[0].text.strip()
                
                if not tdList[0] :
                   break
                for i in range(1,6) :
                   tdList[i] = tdList[i].text
                tdList[1] = tdList[1].replace("\n","")
                tdList[1] = tdList[1].replace("\t","")
                tdList[1] = re.sub(r'\[[^]]*\]', '', tdList[1])
                temp = pd.DataFrame({'date' : tdList[0],'title' : tdList[1], 'view' : int(tdList[3]), 'like' : int(tdList[4]),'dislike' : (tdList[5]), 'code' : code}, index = [0])

                df = df.append(temp)

        return(df)

if __name__ == "__main__":
    discuss = Discuss()
    df  = discuss.update(5930)

    df = df.sort_values(by='like', ascending=False)
    df = df.drop_duplicates(['title'])
    df.index = list(range(len(df)))
    print(df)
    documents = df['title'].values.tolist()[:100]
    print(documents)
    input_document  = ""
    for sentence in documents :
        input_document += sentence+". "
    input_document = [input_document]
    sentiment_analysis_example(client, input_document)