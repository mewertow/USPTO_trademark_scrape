# Python USPTO Trademark Scraper
Simple scraper using selenium to run a trademark clearance search on the USPTO website. Pulls out Goods & Services data, serial numbers, and word marks for all entries, then saves in a .csv file.  

## Install Dependencies: 
`pip install -r requirements.txt`

## Dependencies 
- [Numpy](https://pypi.org/project/numpy/)
- [Pandas](https://pandas.pydata.org/) 
- [Selenium](https://www.selenium.dev/)
- [Requests](https://requests.readthedocs.io/en/master/)
- You must download the appropriate selenium chrome webdriver - (incl. is chrome 87). You can find [chrome webdrivers here] https://chromedriver.chromium.org/downloads.
- [Python 3.8](https://www.python.org/downloads/release/python-380/)

## Flow 
1. Run the file from terminal:  `python uspto_tm_scrape.py`
2. Enter your search term. _Note: Can't be empty._ 
4. Sit back and relax

## Notes
Only tested on windows 10 (version 10.0.18363)

# TODO: Improvements
1. Iterate over data table only once, pulling out data as you go, for significant speed improvement. 
2. Append an existing .csv file rather than dump all data from pandas dataframe at the end - in case the browser window closes, all data is lost. 
3. Add a list of filter terms for the G&S text to pull out relevant entries - e.g., 'media' or 'video games' 
