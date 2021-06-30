import httplib2
import os
from apiclient import discovery
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
scopes = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/spreadsheets"
]
secret_file = os.path.join(os.getcwd(), 'credentials.json')

credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
sheets_service = discovery.build('sheets', 'v4', credentials=credentials)
drive_service = discovery.build('drive', 'v3', credentials=credentials)


from typing import Optional
from fastapi import FastAPI

app = FastAPI()
EMAIL = 'wavelit1@gmail.com'

@app.get('/')
def get_home():
    return {
        'status' : 200
    }

@app.get('/get-spreadsheet/{spreadsheet_id}')
def get_spreadsheet(spreadsheet_id):
    import gspread
    from pprint import pprint
    from gspread.models import Cell, Spreadsheet

    scope = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    json_key_absolute_path = "credentials.json"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key_absolute_path, scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet_list = spreadsheet.worksheets()

    value = {"sheet_id":[],"sheet_title":[]}
    for i in worksheet_list:
        value["sheet_id"].append(i.id)
        value["sheet_title"].append(i.title)

    return {
        'worksheet_list' : value
    }

@app.get('/get-value/{spreadsheet_id}/{sheet_title}')
def get_value(spreadsheet_id,sheet_title):
    import gspread
    from pprint import pprint
    from gspread.models import Cell, Spreadsheet

    scope = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    json_key_absolute_path = "credentials.json"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_key_absolute_path, scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(sheet_title)
    worksheet.get_all_values()
    value = []
    value.append(worksheet.get_all_values())

    return {
        'value' : value
    }
