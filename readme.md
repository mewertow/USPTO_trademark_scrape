# PythonMetaCriticScraper
Simple BeautifulSoup scraper to pull out Goods & Services data from a simple USPTO search. 
[Markdown tips](https://www.markdownguide.org/basic-syntax).

## Dependencies 
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) - `pip install beautifulsoup4`
- [Numpy](https://pypi.org/project/numpy/) - `pip install numpy`
- python 3.8 req'd


# Goal
1. Start at the search page for live entries of Nova (http://tmsearch.uspto.gov/bin/showfield?f=toc&state=4807%3Aua2i6e.3.1)
2. Crawl through each entry (50 per page, 1392 pages) and click the hyperlink to go to the trademark page. Record the serial number. 
    1. In the trademark page, under the goods & services entry, pull all text starting from "G & S:" UP TO the first period "." - semicolons separate G&S entries. Store in column next to serial number.  
3. When reach entry #50, go to next page and repeat. Simply add 50 to the index at end of the http address. If index > 1351, stop.    

## Flow 
1. Run the file as main:  `python uspto_tm_scrape.py`
2. Enter your game title. _Note: Any title must match exactly with a metacritic entry, it's basic search functionality._
3. Enter your console options as space-separated entries, or simply hit return to search all consoles in the list. 
4. Receive data with your eyes



http://tmsearch.uspto.gov/bin/showfield?f=toc&state=4807%3Aua2i6e.3.51
http://tmsearch.uspto.gov/bin/showfield?f=toc&state=4807%3Aua2i6e.3.101
http://tmsearch.uspto.gov/bin/showfield?f=toc&state=4807%3Aua2i6e.3.1351
