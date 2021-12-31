from oauth2client.service_account import ServiceAccountCredentials
import gspread
import gspread_dataframe as gd
import pandas as pd
from df2gspread import df2gspread as d2g
import pickle

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/Andrew/Desktop/CalBasketballData/cal-basketball-data-scraper-private-key.json', scope)

client = gspread.authorize(creds)

spreadsheet_key = '16G1DxZy2-X5wLcqjWRRWxHaZo0bcXl2TOHFukrhMEhY'

#grab DataFrame from data_collection
with open('pickledata.p', 'rb') as fh:   #you need to use 'rb' to read
    df = pickle.load(fh)

#.worksheet("SHEET NAME")
sheet = client.open("Cal Post Game Analytics").sheet1
wks_name = 'Sheet1'

#flips sheets into pandas DataFrame to append data_collection grab
existing = gd.get_as_dataframe(sheet)
existing = pd.DataFrame(sheet.get_all_records())
existing.drop([],axis=1,inplace=True)
updated = existing.append(df)
gd.set_with_dataframe(sheet, updated)


d2g.upload(df, spreadsheet_key, wks_name, credentials=creds, row_names=True)