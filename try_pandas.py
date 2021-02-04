from selenium import webdriver

import pandas as pd
import time
import os
import csv
import datetime

year = int(input("請輸入年度: "))
month = int(input("請輸入月份: "))

first_row = []
start_time = datetime.datetime.now()  # 計算程式執行時間
start_time = start_time.strftime("%Y-%m-%d %H:%M:%S%p")
first_row.append("程式執行時間")
first_row.append(start_time)

# 紀錄當前年度和月(會呈現在excel第一列)
input_time = []
input_time.append("")
yearString = str(year) + "年度"
input_time.append(yearString)
monthString = str(month) + "月"
input_time.append(monthString)

options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path="/Users/vincenthsieh/Downloads/chromedriver", chrome_options=options)

driver.get(f'https://mops.twse.com.tw/nas/t21/sii/t21sc03_{year}_{month}_0.html')

python_button = driver.find_element_by_css_selector('[value="另存CSV"]').click()
time.sleep(3)
os.rename(f"t21sc03_{year}_{month}.csv", f"{year}_{month}.csv")


df = pd.read_csv(f"{year}_{month}.csv")

dll = []
for i in range(len(df)):
    dl = []
    dl.append(df["公司代號"][i])
    dl.append(df["公司名稱"][i])
    dl.append(df["營業收入-當月營收"][i])
    dl.append(df["營業收入-上月營收"][i])
    dl.append(df["營業收入-上月比較增減(%)"][i])
    dl.append(df["營業收入-去年同月增減(%)"][i])
    dll.append(dl)


with open(f'{year}_{month}.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    # 建立 CSV 檔寫入器
    writer = csv.writer(csvfile)
    # 寫入一列資料
    writer.writerow(first_row)
    writer.writerow(input_time)  # 寫入檔案的年度和月份
    writer.writerow(["公司代號","公司名稱", "當月營收", "上月營收", "MOM", "YOY"])
    # 寫入另外幾列資料
    for i in range(len(dll)):
        writer.writerow(dll[i])
#os.remove(f"{year}_{month}.csv")