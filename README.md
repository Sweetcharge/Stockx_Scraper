# Stockx sales scraper
Scrapes StockX and outputs the user's sale history into a CSV file. Very useful for come tax season. This was my first 
real project dealing with requests and JSON so my style of code may seem "amateur" but I'm still learning. Hopefully this
makes everyone's lives easier! Just run script and all your sales are recorded on excel!

NOTE: In your spreadsheet, any red number means you LOST money through that transaction; you got a negative number.

# Requirements
- Python 3
- Requests module

# Common errors

"Key error" 
 Either you didn't put in your credentials in the script or you were sending too many requests to StockX within a short period of time (This is usually the case). Try again with a different IP or wait a couple of minutes.

# Notes
- Make sure you've installed everything you've needed to install; refer to the requirements. 
 
- Don't forget to add your credentials inside the script! This is super important or else the script wont run!

- In order to run the script, for Mac users (should be the same for Window users too):
  1. In terminal type: 
  
     python ***drag and drop the script in here***


- The created file will be called "StockX_Sales.csv"

- The total profit will be at the bottom

