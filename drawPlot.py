import pymysql
from dateutil.parser import parse
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates

def selectDB():
    mydb = pymysql.connect(host='147.46.247.204',
                        user='root',
                        password='blockchain',
                        db='crawling',
                        charset='utf8')

    sql = "SELECT date, count(*) FROM telegram where type = 'moonbird' group by date"
    

    with mydb:
        with mydb.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
            x_values = []
            y_values = []
            #######################################plot 그릴 때의 기간 입력
            start = "2022-05-31"
            last = "2022-06-06"
            ###########################################################
            for data in result:
                if data[0] <= start:
                    print("break!")
                    break;
                if data[0] > last:
                    continue;
                
                x_values.append(data[0])
                y_values.append(data[1])
            
            x_values.reverse() #날짜가 거꾸로나와서 reverse
            y_values.reverse()
            print(x_values)
            print(y_values)
            print()
            pos = 0
            noMsgFlag = False

            start_date = datetime.strptime(start, "%Y-%m-%d")
            last_date = datetime.strptime(last, "%Y-%m-%d")
            while start_date <= last_date:
                dates = start_date.strftime("%Y-%m-%d")
                # print(dates)
                if dates < x_values[pos] or dates > x_values[pos]:
                    print("pos:",pos)
                    print("x_values[pos]:",x_values[pos])
                    if noMsgFlag:
                        x_values.insert(len(x_values),dates)
                        y_values.insert(len(y_values),0)
                    else:
                        x_values.insert(pos,dates)
                        y_values.insert(pos,0)
                    # pos=pos+1
                    # print(x_values)
                
                pos=pos+1
                if pos >= len(x_values):
                    pos = len(x_values) - 1
                    noMsgFlag = True
                # 하루 더하기
                start_date += timedelta(days=1)
                
                
            plt.figure()
            plt.plot(x_values, y_values)
            # plt.xticks(rotation=45) #45도로 x축 회전
            plt.xticks(fontsize=8)
            plt.title("MoonBird",fontsize = 20)
            plt.xlabel("Date",fontsize=12)
            plt.ylabel("The number of messages", fontsize=12)
            # ax = plt.gca()
            # ax.xaxis.set_major_locator(dates.DayLocator(interval=7))
            plt.show()
selectDB()