
import json
from Spreadsheets import Spreadsheet
import requests
from datetime import datetime
from dotenv import load_dotenv
from urls_list import URLS
import generator


def getSetting():
    try:
        f = open('setting.json', 'r')
        data = json.loads(f.read())
        f.close()
        return data
    except Exception as e:
        return {"endRow": None, "spreadsheetId": None}

def setSetting(data):
    try:
        f = open('setting.json', 'w')
        f.write(json.dumps(data))
        f.close()
        return data
    except Exception as e:
        return {"endRow": None, "spreadsheetId": None}
    

if __name__ == "__main__":
    # Подключение .env
    load_dotenv()
    
    # Файл, полученный в Google Developer Console
    CREDENTIALS_FILE = 'creds.json'

    setting = getSetting()
    gen = generator.generate()
    if setting['spreadsheetId'] is not None and setting['endRow'] is not None:
        ss = Spreadsheet(CREDENTIALS_FILE, debugMode=False)
        ss.setSpreadsheetById(setting['spreadsheetId'])
    
        for index, value in enumerate(URLS):
            print(value)
            dataApi = requests.get(
                "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}&strategy=desktop".format(value))
            data = json.loads(dataApi.text)
            desktop = float(data["lighthouseResult"]["categories"]["performance"]["score"]) * 100

            dataApi = requests.get(
                "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}&strategy=mobile".format(value))
            data = json.loads(dataApi.text)
            mobile = float(data["lighthouseResult"]["categories"]["performance"]["score"]) * 100

            dt = datetime.now()

            rangeData = generator.generateRangeSheets(gen)
            ss.prepare_setValues(rangeData[0] + str(setting['endRow']) + ':' + rangeData[1] + str(setting['endRow']),
                                 [[datetime.now().strftime("%d.%m.%y %H:%M"), desktop, mobile]])

        ss.runPrepared()

        setting['endRow'] = setting['endRow'] + 1
        setSetting(setting)
        
        
    
    