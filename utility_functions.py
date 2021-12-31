import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

#collect & process data based on GAME ID
def processor(game_id):
    url = "https://www.espn.com/mens-college-basketball/matchup?gameId=" + str(game_id)
    r = requests.get(url)
    webpage = bs(r.content)

    #create dictionary for CAL & opponent with respective scores
    team_name = [name.string for name in webpage.find_all("td", attrs={"class", "team-name"})]
    score = [float(final_score.string) for final_score in webpage.find_all("td", attrs={"class", "final-score"})]

    team_score = dict(zip(team_name, score))

    #determine opponent
    for team in team_name:
        if team != "CAL":
            opponent = team

    #locate table for main data regarding game
    table = webpage.select("table.mod-data")[0]

    #create column_names and locate the rows of the table

    column_names = (list(team_score.keys()))
    #columns = table.find_all("td", string=re.compile("[A-Za-z%]+"))
    #column_names = [c.get_text().strip() for c in columns]

    table_rows = table.find("tbody").find_all("tr")

    #accumulate all the table_rows into one list
    row_names, l = [], []
    for tr in table_rows:
        td = tr.find_all("td")
        #row: [STAT_NAME, NUM1, NUM2]
        row = [tr.get_text().strip() for tr in td]
        #.append([NUM1, NUM2])
        l.append(row[1:])
        #.append([STAT_NAME])
        row_names.append(row[0])

    #create data table with column_names and rows within table.mod-data
    df = pd.DataFrame(l, columns=column_names)

    #searches a string with - and seperates elements from either side into a list
    def try_convert(val): 
        hyphen_index = val.index("-")
        return [val[:hyphen_index], val[hyphen_index + 1:]]

    #append new rows for FGA, FGM, 3PTA, 3PTM, FTA, FTM for later calculations in MAKES-ATTEMPT format
    for index in df.index:
        if re.search("-", df.loc[index, "CAL"]) and re.search("-", df.loc[index, opponent]):
            #multiple assignment with try_convert to extract attempts and makes 
            makes_cal, att_cal = try_convert(df.loc[index, "CAL"])[0], try_convert(df.loc[index, "CAL"])[1]
            makes_opp, att_opp = try_convert(df.loc[index, opponent])[0], try_convert(df.loc[index, opponent])[1]
            
            #assigns current row with makes
            df.loc[index, "CAL"], df.loc[index, opponent] = makes_cal, makes_opp
        
            #append new row with attempts, increasing index to reorder later
            df2 = pd.DataFrame({'CAL': att_cal, opponent: att_opp}, index=[index + .1])
            df = df.append(df2, ignore_index = False)

    #reorder rows with increasing index
    df = df.sort_index().reset_index(drop=True)

    #adds FGA, FGM, 3PTA, 3PTM, FTA, FTM row names
    row = []
    def add_makes_att(lst, new_lst):
        for stat in lst:
            if re.search("FG|3PT|FT", stat):
                new_lst.append(stat + "M")
                new_lst.append(stat +"A")
            else:
                new_lst.append(stat)
        return new_lst

    row_names = add_makes_att(row_names, row)

    #set row indexes as STAT_NAME within row
    df.index = row_names

    #turns all stats into float, tranpose matrix
    df["CAL"] = pd.to_numeric(df["CAL"], downcast="float")
    df[opponent] = pd.to_numeric(df[opponent], downcast="float")
    df = df.T

    #calculates +/-
    def net(cal, opp):
        if cal - opp > 0:
            return "+" + str(cal - opp)
        elif opp - cal > 0:
            return "-" + str(opp - cal)
        else:
            return 0

    #create a list respresenting calculations for the game
    poss = df.loc['CAL', 'FGA']-df.loc['CAL', 'Offensive Rebounds']+df.loc['CAL', 'Total Turnovers']+.475*df.loc['CAL', 'FTA']
    calc = [opponent, poss, team_score[opponent]/poss, (df.loc[opponent, 'FGM']+.5*df.loc[opponent, '3PTM'])*100/df.loc[opponent, 'FGA'], df.loc['CAL', 'Defensive Rebounds']*100/(df.loc['CAL', 'Defensive Rebounds']+df.loc[opponent, 'Offensive Rebounds']), df.loc[opponent, 'Total Turnovers']*100/poss, df.loc[opponent, 'Field Goal %'], df.loc[opponent, 'Three Point %'],(df.loc[opponent, 'FTA']*100/df.loc[opponent, 'FGA'], df.loc[opponent, 'FTM']*100/df.loc[opponent, 'FTA']), team_score['CAL']/poss, (df.loc['CAL', 'FGM']+.5*df.loc['CAL', '3PTM'])*100/df.loc['CAL', 'FGA'], df.loc['CAL', 'Offensive Rebounds']*100/(df.loc[opponent, 'Defensive Rebounds']+df.loc['CAL', 'Offensive Rebounds']), df.loc['CAL', 'Total Turnovers']*100/poss, df.loc['CAL', 'Field Goal %'], df.loc['CAL', 'Three Point %'],(df.loc['CAL', 'FTA']*100/df.loc['CAL', 'FGA'], df.loc['CAL', 'FTM']*100/df.loc['CAL', 'FTA']), net(df.loc['CAL', 'Offensive Rebounds']+df.loc["CAL", 'Defensive Rebounds'], df.loc[opponent, 'Offensive Rebounds']+df.loc[opponent, 'Defensive Rebounds']), net(df.loc['CAL', '3PTM'], df.loc[opponent, '3PTM'])]
    return calc

#find date of game
def get_date(game_id):
    url = "https://www.espn.com/mens-college-basketball/game/_/gameId/" + str(game_id)
    r = requests.get(url)
    webpage = bs(r.content)
    date = webpage.find("header", attrs={"class", "top-stories__story-header"}).find("span", attrs={"class", "date"}).get_text()
    return date

#rounds data based on stat parameters
def clean(series):
    if series.name == "Game" or series.name == "Reb +/-" or series.name == "3pt +/-":
        return series
    elif series.name == "OER" or series.name == "DER":
        return series.astype('float64').round(2)
    elif series.name == "Def FT RATE, %" or series.name == "Off FT Rate, %":
        #encounters tuple data structure of two valued stat
        return series.apply(lambda stats: tuple(map(round, stats)))
    else:
        return series.astype('int32')