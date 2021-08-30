import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import time
starttime = datetime.datetime.now()

def getAmount(stock_id):
    url = f"https://www.cnyes.com/twstock/Technical.aspx?code={stock_id}"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    req5 = soup.find_all("tr", class_="thbtm2")[1].select_one("tr").find_all("td")[3]
    req20 = soup.find_all("tr", class_="thbtm2")[1].select_one("tr").find_all("td")[5]
    return int(req5.text), int(req20.text)

with open("five_ten.csv", "r") as csvfile:
    count = 0
    l = csvfile.readlines()
    for i in range(3, len(l)):
        l[i] = l[i].split(',')
        try:
            req5, req20 = getAmount(l[i][0])
            dev = round((req5/req20),2)
            print(f"{l[i][0]}: {req5}, {req20}, {dev}")
        except: 
            count += 1
            print(f"{l[i][0]}: none")


print("error", count)  # 43
endtime = datetime.datetime.now()
print (endtime - starttime) 
            