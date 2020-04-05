import argparse
import json
import os
import sys

from Spreadsheets import Spreadsheet
import requests
from datetime import datetime
from dotenv import load_dotenv
from urls_list import URLS
import generator

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--site', default="unknown")
    parser.add_argument('-e', '--email', default=os.environ.get('EMAIL_USER'))
    
    return parser

def getSetting():
    try:
        f = open('setting.json', 'r')
        data = json.loads(f.read())
        f.close()
        return data
    except Exception as e:
        return {"endRow": None, "spreadsheetId": None}


if __name__ == "__main__":
    # Подключение .env
    load_dotenv()

    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    # Файл, полученный в Google Developer Console
    CREDENTIALS_FILE = 'creds.json'
    
    SITE = namespace.site
    USER = namespace.email
    
    # setting = getSetting()
    # if setting.get("spreadsheetId", None) is None:
    #     # Создание нового отчета и его расшаривание
    #     ss = Spreadsheet(CREDENTIALS_FILE, debugMode = True)
    #     ss.create(f"Отчет {SITE}", "Данные")
    #     ss.shareWithEmailForWriting(namespace.email)
    
    # with open("report_file.json", "w", encoding="utf-8") as file:
    #     json.dump({"sheetId": ss.spreadsheetId}, file)
    
    # Чтение уже готового файла
    ss = Spreadsheet(CREDENTIALS_FILE, debugMode=False)
    ss.setSpreadsheetById('1jZLKUOsPwxmaZSGjAVBxuG5a0lM30yDmqYw_RK7r86k')

    gen = generator.generate()
    for index, value in enumerate(URLS):
        rangeData = generator.generateRangeSheets(gen)
        print(rangeData[0]+'1:'+rangeData[1]+'1')

        ss.prepare_mergeCells(rangeData[0]+'1:'+rangeData[1]+'1')
        ss.prepare_setValues(rangeData[0]+'1:'+rangeData[1]+'1', [[str(value)]])
        ss.prepare_setValues(rangeData[0]+'2:'+rangeData[1]+'2', [["Дата/Время", "Desktop", "Mobile"]])

        ss.prepare_setCellsFormat(rangeData[0] + '1:' + rangeData[1] + '2', {'horizontalAlignment': 'CENTER'})

        ss.prepare_setCellsBorders(rangeData[0]+'1:'+rangeData[1]+'10', 'right', 'SOLID', 4)
    ss.runPrepared()
 




