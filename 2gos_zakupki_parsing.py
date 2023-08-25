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
for i in range(1,10):   
    url = "https://www.goszakup.gov.kz/ru/registry/rqc?count_record=50&page=" + str(i)
    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    all_trs = soup.find("div",class_= "panel-body")[1].find('tbody').find_all('tr')

    for item in all_trs:
        link = item.find('a').get("href")
        all_links.append(link)

    sleep(random.random()* 2.5)

with open(f"gos_zakupki.csv", "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            "Наименование",
            "БИН организации",
            "ФИО руководителя",
            "Amount(BTC)",
            "ИИН руководителя",
            "Полный адрес организации"
        )
    )

list_of_companies = []

for link in all_links:
    req = requests.get(url= link, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, "lxml")

    try:
        table1 = soup.find("div",class_= "panel-body")[0].find('tbody').find_all("tr")

        try:
            BIN_organizazii = table1[5].find("td").text
        except Exception:
            BIN_organizazii = None
        try:
            Naimenovanie = table1[8].find("td").text
        except Exception:
            Naimenovanie = None
    except Exception:
        BIN_organizazii = None
        Naimenovanie = None
    
    try:
        table2 = soup.find("div",class_= "panel-body")[2].find('tbody').find_all("tr")

        try:
            IIN_rukovoditelya = table1[0].find("td").text
        except Exception:
            IIN_rukovoditelya = None
        try:
            FIO_rukovoditelya = table1[2].find("td").text
        except Exception:
            FIO_rukovoditelya = None
    except Exception:
        IIN_rukovoditelya = None
        FIO_rukovoditelya = None
   
    try:
        Adress = soup.find("div",class_= "panel-body")[3].find('tbody').find_all("tr")[1].find_all('td')[2].text
    except Exception:
        Adress = None



    if Naimenovanie not in list_of_companies:
        with open(f"gos_zakupki.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    Naimenovanie,
                    BIN_organizazii,
                    IIN_rukovoditelya,
                    FIO_rukovoditelya,
                    Adress
                )
            )
    else:
        continue
    list_of_companies.append(Naimenovanie)

    sleep(random.random()* 2.5)