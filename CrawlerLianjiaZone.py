import urllib.request
import requests
import os
import re
import psycopg2
import json
import time

url = "https://hz.lianjia.com/api/headerSearch?cityId=330100&cityName=杭州&channel=xiaoqu&q=&keyword=世纪新城";

def getLianjiaZoneUrl(cityId,cityName,keyword):
    return "https://hz.lianjia.com/api/headerSearch?cityId="+cityId+"&cityName="+cityName+"&channel=xiaoqu&q=&keyword="+keyword;


def getOneKeyWord():
    conn = psycopg2.connect(database="superpower", user="postgres", password="123456", host="localhost", port="5432");
    cur = conn.cursor();
    cur.execute("SELECT t.region_id,t.name from gaode_residential_region t where t.region_id not in (select DISTINCT kl.gaode_regionid from lianjia_zone_code_data kl UNION select k.gaode_regionid from lianjia_zone_code_disable k) limit 1;");
    keyData = cur.fetchall();
    regionId=keyData[0][0];
    regionName=keyData[0][1];
    a1 = re.compile('\(.*\)')
    regionName = a1.sub('', regionName)
    result=[regionId,regionName];
    return result;



def download():
    requestDate=getOneKeyWord();
    if(requestDate[1]!= None):
        url=getLianjiaZoneUrl('330100','杭州',requestDate[1]);
        print(url);
        try:
            res = requests.get(url, timeout=30).content;
            total_json = json.loads(res);
            listJson = total_json.get('data').get('data').get('result');
            poiCount = len(listJson);
            if poiCount > 0:
                print(poiCount);
                for poi in listJson:
                    print(poi);
                    title=poi.get('title');
                    keyword=poi.get('keyword');
                    channel = poi.get('channel');
                    preUnitPirce= poi.get('preUnitPirce');
                    count = poi.get('count');
                    region = poi.get('region');
                    communityId = poi.get('communityId');
                    url = poi.get('url');
                    sql= "INSERT INTO lianjia_zone_code_data(title, keyword, pre_unitpirce, region, community_id, url,gaode_regionid)VALUES('"+title+"', '"+keyword+"', '"+str(preUnitPirce)+"', '"+region+"', '"+str(communityId)+"', '"+url+"', '"+requestDate[0]+"');"
                    conn = psycopg2.connect(database="superpower", user="postgres", password="123456", host="localhost",
                                            port="5432");
                    cur = conn.cursor();
                    try:
                        cur.execute(sql);
                    except Exception as e:
                        print(e);
                    conn.commit();
                    cur.close();
                    conn.close();
            else:
                sql1 = "INSERT INTO lianjia_zone_code_disable(gaode_regionid, region_name)VALUES('" + requestDate[
                    0] + "', '" + requestDate[1] + "')";
                conn = psycopg2.connect(database="superpower", user="postgres", password="123456", host="localhost",
                                        port="5432");
                cur = conn.cursor();
                try:
                    cur.execute(sql1);
                except Exception as e:
                    print(e);
                conn.commit();
                cur.close();
                conn.close();
        except Exception as e:
            print(e);
            sql1= "INSERT INTO lianjia_zone_code_disable(gaode_regionid, region_name)VALUES('"+requestDate[0]+"', '"+requestDate[1]+"')";
            conn = psycopg2.connect(database="superpower", user="postgres", password="123456", host="localhost",
                                    port="5432");
            print(sql1);
            cur = conn.cursor();
            try:
                cur.execute(sql1);
            except Exception as e:
                print(e);
            conn.commit();
            cur.close();
            conn.close();




def batchGetResidential():
    a = 1;
    while a == 1:
        download();
        time.sleep(5);

batchGetResidential();
