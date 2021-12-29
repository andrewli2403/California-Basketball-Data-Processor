from oauth2client.service_account import ServiceAccountCredentials
import gspread

import pandas as pd


scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('cal-basketball-data-scraper-private-key.json', scope)

client = gspread.authorize(creds)

#.worksheet("SHEET NAME")
sheet = client.open("Cal Post Game Analytics").sheet1

sheet.update_cell(2, 4, "asdf")