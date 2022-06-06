import pymysql.cursors # 접속 # 비밀번호가 포함되어 있기 때문에 보통 config파일에서 key값으로 부른다. 
import pymysql
import json
import sys
from dateutil.parser import parse
from datetime import datetime

def createTable():
    mydb = pymysql.connect(
        host = "147.46.247.204", #ex) '127.0.0.1' port=3306, 
        user = "root", #ex) root
        port = 3306,
        password = "blockchain",
        charset = 'utf8',
        db='crawling'
    ) 
    # Cursor Object 가져오기 
    # sql = '''CREATE TABLE telegram (
    #     type varchar(255) NOT NULL,
    #     id varchar(255) NOT NULL PRIMARY KEY,
    #     name varchar(255),
    #     date varchar(255),
    #     views varchar(255)
    #     forwards varchar(255),
    #     replies varchar(255)        
    #     )
    #     '''
    sql = '''CREATE TABLE user (
        id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name varchar(255),
        email varchar(255)
        )
        '''
    with mydb:
        with mydb.cursor() as cur:
            cur.execute(sql)
            mydb.commit()

def insertsql_from_json():
    mydb = pymysql.connect(
        host = "147.46.247.204", #ex) '127.0.0.1' port=3306, 
        user = "root", #ex) root
        port = 3306,
        password = "blockchain",
        charset = 'utf8',
        db='crawling'
    ) # Cursor Object 가져오기 
    curs = mydb.cursor()

    #geoJson 가져오기 
    with open('./channel_messages_bayc.json',encoding='utf-8') as json_file: 
        json_data = json.load(json_file) 
        #json의 key로 접근 
        # print(json_data)
        # #json_line : json 객체를 가지는 Array 
        # json_line = json_data[10000] # 하나의 메세지 전체
        # json_line = json_data[0]['id'] #하나의 메세지 안에 id값만 return
        
        # print(json_line)
        dataType = "bayc"
        for i in range (sys.maxsize):
        # for i in range (1000):
            try:
                json_line = json_data[i] # 하나의 메세지 전체
                # print(json_line)
                # print()
                json_id = json_line['id'] 
                json_views = json_line['views']
                json_forwards = json_line['forwards'] 
                str_date = json_line['date']
                # print(json_line['replies'])
                # print(type(str_date))
                json_date = parse(str_date)
                json_date = json_date.date()
                if json_line['replies'] is None:
                    json_replies = 0
                else:
                    json_replies = json_line['replies']['replies']
                if json_views is None:
                    json_views = 0
                if json_forwards is None:
                    json_forwards = 0
                # print(json_forwards)
                # print(json_replies)
                # print(json_id, json_views, json_forwards,json_date,json_replies)
                sql = "INSERT INTO telegram(type,id,date,views,forwards,replies) VALUES (%s,%s,%s,%s, %s, %s)" 
                val = (dataType,str(json_id),str(json_date),str(json_views),str(json_forwards),str(json_replies)) 
                curs.execute(sql, val) 
                mydb.commit() 
                
            except IndexError:
                print("@list index out of range",i)
                break
            except KeyError:
                print("keyError!")
                continue
        print("done")
        
        # print(json_line)
        # for a in json_line: 
        #     lon = a
        #     # lat = a['peer_id'][1] 
            
        #     print(lon)
        #     # print(lat)            
        #     # sql = "INSERT INTO loadpoint(lat, lon) VALUES (%s, %s)" 
        #     # val = (float(lat), float(lon)) 
            
        #     # curs.execute(sql, val) 
        #     # conn.commit() 
    print(curs.rowcount, "record inserted") 
            
# createTable()
insertsql_from_json()
