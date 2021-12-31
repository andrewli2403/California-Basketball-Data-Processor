# California Basketball Data Processor
Utilizes BeautifulSoup, pandas, and crontab to automate data collection and statistical processing for California Men's Basketball.

# Main Files
data_processor.ipynb & utility_function.py: web scrapes [college basketball game](https://www.espn.com/mens-college-basketball/matchup?gameId=401281460) statistics and creates pandas DataFrame for calculated analytics

data_collection.py: aggregates calculated analytics 5 hours after gametime and updates season analytics onto a pickle file

uploader.py: displays season analytics using Google Sheet API

crontab schedule: set to run at every other hour