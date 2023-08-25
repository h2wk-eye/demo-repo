import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"
}
all_links = []
for i in range(1,11):   
    url = "https://www.goszakup.gov.kz/ru/registry/rqc?count_record=50&page=" + str(i)
    req = requests.get(url, headers=headers, verify=False)
    src = req.text

    soup = BeautifulSoup(src, "html.parser")
    
    div_body = soup.find_all('div', class_ = 'panel-body')[1]
    all_trs = soup.find_all("div", class_="panel-body")[1].find('tbody').find_all('tr')
    # print(all_trs)
    for item in all_trs:
        # print(item.find('a').get("href"))
        link = item.find('a').get("href")
        all_links.append(link)
    soup = BeautifulSoup
    sleep(random.random()* 2)

with open(f"gos_zakupki.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            "Наименование",
            "БИН организации",
            "ФИО руководителя",
            "ИИН руководителя",
            "Полный адрес организации"
        )
    )

list_of_companies = []

for link in all_links:
    req = requests.get(url= link, headers=headers, verify= False)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    try:
        table1 = soup.find("div", class_="panel-body").find_all("tr")
        print(table1)
        try:
            BIN_organizazii = table1[5].find("td").text
        except Exception:
            BIN_organizazii = None
        try:
            Naimenovanie = table1[7].find("td").text
        except Exception:
            Naimenovanie = None
    except Exception:
        BIN_organizazii = None
        Naimenovanie = None
    
    try:
        table2 = soup.find_all("div", class_="panel-body")[2].find_all("tr")

        try:
            IIN_rukovoditelya = table2[0].find("td").text
        except Exception:
            IIN_rukovoditelya = None
        try:
            FIO_rukovoditelya = table2[2].find("td").text
        except Exception:
            FIO_rukovoditelya = None
    except Exception:
        IIN_rukovoditelya = None
        FIO_rukovoditelya = None
   
    try:
        Adress = soup.find_all("div", class_="panel-body")[3].find_all('tr')[1].find_all('td')[2].text.strip().replace(',', ' ')
    except Exception:
        Adress = None



    with open(f"gos_zakupki.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                Naimenovanie,
                BIN_organizazii,
                FIO_rukovoditelya,
                IIN_rukovoditelya,
                Adress
            )
        )


    sleep(random.random()* 2)

import pandas as pd

# reading the csv file
cvsDataframe = pd.read_csv('gos_zakupki.csv')

# creating an output excel file
resultExcelFile = pd.ExcelWriter('gos_zakupki.xlsx')

# converting the csv file to an excel file
cvsDataframe.to_excel(resultExcelFile, index=False, header=True)

# saving the excel file
resultExcelFile._save()