# is-206-lederman-final-project
For my final project in SI206!

Data Sources:
- I scraped and crawled the Yelp website to obtain data regarding the top 10 restaurants from each state in the US
- My project does not utilize any API's so no API Key's or Client Secrets are needed
- I scraped the top ten restaurants from every state on Yelp, crawling into each of the 10 restaurants to scrape price and review data. By scraping and crawling, I was able to obtain data such as maximum price/person, address, restaurant name, restaurant type, restaurant state, a single restaurant review, and the restaurant's star rating.

Code Structure:
- Class:
  - "class Restaurant"


- Key Functions:
  - The "get_yelp_data()" function allows me to use BeautifulSoup and caching in order to scrape, crawl, and obtain the data from the Yelp website. The caching code stores the data as a json file, allowing it to be accessed quickly while the program is being executed.
  - The "init_database()" function creates an sqlite3 database with two tables, Restaurants and Reviews. The data obtained in the "get_yelp_data()" function is added to these two databases using the "insert_data_rest()" function and "insert_data_review()" function.
  - The "populate_db" function allows the two databases to be populated by US state data from Yelp when the function is initialized at the bottom of the final_project_yelp.py file. Once the data is loaded, this function can be uninitialized, and the "yelp_interactive_search()" function is ready for use.
  - The "yelp_interactive_search()" function prompts a user to choose how they would like their data grouped (either by restaurant state or restaurant type) and how they would like such grouping ordered (either by average maximum price/person or average star rating). The resulting data is then formed into one of these 4 data combinations as a bar graph.
