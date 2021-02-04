# 引用函示庫
import requests
from bs4 import BeautifulSoup
import csv
import datetime

# 處理資料
List = []
def add_things(h, last):
    for i in range(1, len(h)):
        stock_list = h[i].split(",")  # 以逗號作為分割
        company = stock_list[3]
        for i in range(1, len(last)):
            if company == last[i].split(",")[3]:
                last_stock_list = last[i].split(",")
                for i in range(10):
                    stock_list[i] = stock_list[i].strip("\"")  # 把 " 刪除
                    last_stock_list[i] = last_stock_list[i].strip("\"")
                temp_list = []
                temp_list.append(stock_list[2])  # 加入股票代號
                temp_list.append(stock_list[3])  # 加入股票名字
                if stock_list[5] != "":
                    temp_list.append(format(int(stock_list[5]), ','))  # 加入當月營收
                else:
                    temp_list.append("None")
                temp_list.append(format(int(stock_list[6]), ','))  # 加入上月營收
                temp_list.append(format(int(last_stock_list[5]), ','))
                temp_list.append(format(int(last_stock_list[6]), ','))
                try:
                    stock_list[8] = float(stock_list[8])  # 加入MOM
                    temp_list.append(round(stock_list[8], 2))
                except:
                    temp_list.append("None")  # 避免有些公司上月營收是 0
                temp_list.append(format(int(stock_list[7]), ','))  # 去年同期營收
                try:
                    stock_list[9] = float(stock_list[9])  # 加入YOY
                    temp_list.append(round(stock_list[9], 2))
                except:
                    temp_list.append("None")
                List.append(temp_list)


#處理使用者輸入介面
while True:
    try:
        year = int(input("請輸入年度: "))  # 如果不是輸入整數會讓使用者重新輸入
        break
    except:
        print("年份格式錯誤，請重新輸入")
while True:
    try:
        month = int(input("請輸入月份: "))  # 如果不是輸入整數會讓使用者重新輸入
         # 如果不是輸入正確月份會讓使用者重新輸入
        if month < 1 or month > 12:
            print("無此月份，請重新輸入")
            continue
        break
    except:
        print("月份格式錯誤，請重新輸入")

first_row = []
start_time = datetime.datetime.now()  # 計算程式執行時間
start_time = start_time.strftime("%Y-%m-%d %H:%M:%S%p")
first_row.append("程式執行時間")
first_row.append(start_time)

# 紀錄當前年度和月(會呈現在excel第一列)
number = []
number.append("")
yearString = str(year) + "年度"
number.append(yearString)
monthString = str(month) + "月"
number.append(monthString)

# 抓上上個月
another_year = year
if month == 1:
    another_year = another_year - 1
    another_month = 11
elif month == 2:
    another_year = another_year - 1
    another_month = 12
else:
    another_month = month - 2

# 抓上市公司資料，透過網頁表格直接進行下載
url_sii = requests.get(f"https://mops.twse.com.tw/nas/t21/sii/t21sc03_{year}_{month}.csv")
url_sii.encoding='utf-8'  # 解碼
url_sii_last = requests.get(f"https://mops.twse.com.tw/nas/t21/sii/t21sc03_{another_year}_{another_month}.csv")
url_sii_last.encoding='utf-8'  # 解碼
add_things(url_sii.text.splitlines(), url_sii_last.text.splitlines())  # 把下載的表格丟進函式處理

# 抓上櫃公司資料，透過網頁表格直接進行下載
url_otc = requests.get(f"https://mops.twse.com.tw/nas/t21/otc/t21sc03_{year}_{month}.csv")
url_otc.encoding='utf-8'  # 解碼
url_otc_last = requests.get(f"https://mops.twse.com.tw/nas/t21/otc/t21sc03_{another_year}_{another_month}.csv")
url_otc_last.encoding='utf-8'  # 解碼
add_things(url_otc.text.splitlines(), url_otc_last.text.splitlines())

with open(f'{year}_{month}.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    # 寫入一列資料
    writer.writerow(first_row)
    writer.writerow(number)  # 寫入檔案的年度和月份
    writer.writerow(["公司代號", "公司名稱", "當月營收", "上月營收", "上上月營收", "上上上月營收", "MOM", "去年同期營收", "YOY"])
    # 寫入另外幾列資料
    for i in range(len(List)):
        writer.writerow(List[i])
