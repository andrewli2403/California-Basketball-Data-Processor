import pandas as pd
from utility_functions import *
import pickle
import sys
from datetime import date, datetime, timedelta
from dateutil.parser import parse

Newlimit = 10000
limit = sys.setrecursionlimit(Newlimit)

#run the code 5 hours after the gametime
exe_time = datetime.today() - timedelta(hours=5)

#collection of game_ids and the respective datetime each game occured at
game_ids = [401373623, 401372480, 401373871, 401372618, 401371841, 401376644, 401372389, 401370905, 401370930, 401372467, 401371139, 401373872, 401371302, 401398909, 401377400, 401377403, 401377407, 401377413, 401377419, 401377429, 401377432, 401377437, 401377446, 401377447, 401377453, 401377457, 401377465, 401377469, 401377483, 401377484, 401377490]
dates = [parse(date) for date in map(get_date, game_ids)]

#uses None as an indicator for the automation process to create a dataframe
game_ids = [None] + game_ids
dates = [None] + dates

for game, date in zip(game_ids, dates):
    if not game or not date:
        #create datatable for this game, corresponding to Post Game Analytics
        columns = ["Game", "Poss", "DER", "Def eFG%", "Def Reb%", "Def TO%", "Def FG%", "Def 3PT%", "Def FT RATE, %", "OER", "Off eFG%", "Off Reb%", "Off TO%", "Off FG%", "Off 3pt%", "Off FT Rate, %", "Reb +/-", "3pt +/-"]
        df = pd.DataFrame([], columns=columns)
    elif exe_time > date:
        row = pd.Series(processor(game), index=df.columns, name=date_convert(date))
        df = df.append(row,ignore_index=False).apply(lambda row: clean(row), axis=0)

#pickle df object
with open('pickledata.p', 'wb') as fh:
    pickle.dump(df, fh)