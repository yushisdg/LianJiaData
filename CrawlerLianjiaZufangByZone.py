import re
from bs4 import  BeautifulSoup
import os
import re
import psycopg2
import requests
import json
import time


def getHtmlByUrl():
    url="https://hz.lianjia.com/zufang/c1811044030452/";
    html_doc = requests.get(url, timeout=30).content
    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8');
    links = soup.find(id='house-lst');

    for ele in links:
        print("----------------------------------------------------------------")
        print(ele.attrs );
        meters=ele.find(class_="meters").contents;
        zone=ele.find(class_="zone").find("span").contents
        region=ele.find(class_="region").contents
        price=ele.find(class_="price").find("span").contents
        updateTime=ele.find(class_="price-pre").contents
        other = ele.find(class_="other").find(class_="con").contents



getHtmlByUrl();