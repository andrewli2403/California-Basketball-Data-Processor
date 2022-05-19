# California Basketball Data Processor
Utilizes BeautifulSoup, pandas, and crontab to automate data collection and statistical processing for California Men's Basketball.

# Main Files
`utility_function.py` (based on `data_processor.ipynb`): web scrapes [college basketball game](https://www.espn.com/mens-college-basketball/matchup?gameId=401281460) statistics and creates pandas DataFrame with calculated analytics

`data_collection.py`: aggregates calculated analytics 5 hours after gametime and updates season analytics onto a pickle file

`uploader.py`: displays season analytics onto [Postgame Analytics](https://docs.google.com/spreadsheets/d/16G1DxZy2-X5wLcqjWRRWxHaZo0bcXl2TOHFukrhMEhY/edit?usp=sharing) via Google Sheet API

crontab schedule: set to run at every other hour

# Result
<img src="images/spreadsheet results" width = 800>

