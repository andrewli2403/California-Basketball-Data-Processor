# California Basketball Data Processor
Automates data collection and statistical processing for University of California, Berkeley Men's Basketball. 

More advanced statistics such as effective Field Goal percentage (eFG%), turnover percentage (TO%), free throw rate were previously calculated by hand. This repository automates the process post-game.

# Main Files
`utility_function.py` (based on `data_processor.ipynb`): web scrapes [college basketball game](https://www.espn.com/mens-college-basketball/matchup?gameId=401281460) statistics and calculates desired statistics.

`data_collection.py`: aggregates calculated statistics 5 hours after gametime and updates season statistics onto a pickle file.

`uploader.py`: displays season analytics onto [Postgame Analytics](https://docs.google.com/spreadsheets/d/16G1DxZy2-X5wLcqjWRRWxHaZo0bcXl2TOHFukrhMEhY/edit?usp=sharing) via Google Sheet API

crontab schedule: set to run at every other hour

# Result
<img src="images/spreadsheet results.png" width = 800>

# Tools
BeautifulSoup4, pandas, crontab.


