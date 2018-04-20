import requests
import sqlite3
import csv
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from bs4 import BeautifulSoup

DBNAME = 'yelp.db'
RESTAURANT_CSV = 'restaurants.csv'
REVIEWS_CSV = 'reviews.csv'

def init_database():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    drop_resturants = 'DROP TABLE IF EXISTS "Restaurants"'
    cur.execute(drop_resturants)
    conn.commit()
    drop_reviews= 'DROP TABLE IF EXISTS "Reviews"'
    cur.execute(drop_reviews)
    conn.commit()

#creates table for Restaurants
    create_restaurants = '''
    CREATE TABLE IF NOT EXISTS 'Restaurants' (
    'ResturantId' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Name' TEXT NOT NULL,
    'Type' TEXT,
    'Address' TEXT,
    'State' TEXT NOT NULL,
    'MaxPrice' INTEGER,
    'Review' TEXT,
    'StarRatings' REAL
    )
    '''
    cur.execute(create_restaurants)
    conn.commit()

    create_reviews = '''
    CREATE TABLE IF NOT EXISTS 'Reviews' (
    'ReviewId' INTEGER PRIMARY KEY AUTOINCREMENT,
    'ResturantId' INTEGER,
    'Review' TEXT
    )
    '''
    cur.execute(create_reviews)
    conn.commit()
    conn.close()



try:
    fref= open('cachedata.json', 'r')
    data = fref.read()
    CACHE_DICT = json.loads(data)
except:
    CACHE_DICT = {}

def get_data_using_cache(base_url):
    unique_ident = base_url
    if base_url in CACHE_DICT:
        return CACHE_DICT[base_url]
    else:
        resp = requests.get(unique_ident)
        CACHE_DICT[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICT)
        fw = open('cachedata.json',"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICT[unique_ident]

class Restaurant:
    def __init__(self, name, type, address, maxprice, starrating, state, review):
        self.name = name
        self.type = type
        self.address = address
        self.maxprice = maxprice
        self.starrating = starrating
        self.state = state
        self.review = review

    def __str__(self):
        return self.name
        return self.type
        return self.address
        return self.maxprice
        return self.starrating
        return self.state
        return self.review


def insert_data_rest():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    f = open(RESTAURANT_CSV, 'r')
    reader = csv.reader(f)
    for x in reader:
        query = '''
        INSERT INTO 'Restaurants' (ResturantId, Name, Type, Address, State, MaxPrice, Review, StarRatings) VALUES (?,?,?,?,?,?,?,?)
        '''
        restaurant_info = (None, x[0], x[1], x[2], x[3], x[4][-2:], x[5], x[6])
        cur.execute(query, restaurant_info)
        conn.commit()
    f.close()
    conn.close()


def insert_data_review():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    f1 = open(REVIEWS_CSV, 'r')
    reader1 = csv.reader(f1)
    id_reviews = cur.execute("SELECT ResturantId, Review FROM Restaurants").fetchall()
    rest_id = None
    for x in reader1:
        for pair in id_reviews:
            if x[0] in pair:
                rest_id = pair[0]
        query = '''
        INSERT INTO 'Reviews' (ReviewId, ResturantId, Review) VALUES (?,?,?)
        '''
        reviews_info = (None, rest_id, x[0])
        cur.execute(query, reviews_info)
        conn.commit()
    f1.close()
    conn.close()


def get_yelp_data(state_abbr):
    base_url = 'https://www.yelp.com/search?find_loc='
    state_url = base_url + state_abbr + '&start=0&cflt=restaurants'
    html = get_data_using_cache(state_url)
    page_soup = BeautifulSoup(html, 'html.parser')
    restaurants = page_soup.find_all('li', class_='regular-search-result')
    rest_state = []
    rest_names = []
    rest_addresses = []
    rest_types = []
    rest_price = []
    reviews = []
    ratings = []
    price_map = {'$': "$10", "$$": "$30", "$$$": "$60", "$$$$": "$61-99"}
    for r in restaurants:
        start_price = r.find('div',class_='main-attributes')
        stars = start_price.find('div', class_='i-stars')
        final_stars = float(stars['title'][:3])
        ratings.append(final_stars)
        price = start_price.find('div', class_='price-category')
        if price.span.span == None:
            final_price = "Not Avaliable."
        else:
            final_price = price.span.span.text.strip()
            last = price_map[final_price]
        rest_price.append(last)
        state = state_abbr
        rest_state.append(state_abbr)
        name_data = r.find('a', class_='biz-name')
        name_url = 'https://www.yelp.com' + name_data['href']
        new_req = requests.get(name_url).text
        new_soup = BeautifulSoup(new_req, 'html.parser')
        review_data = new_soup.find('p', class_='quote')
        if review_data == None:
            content = new_soup.find('div', class_='review-content')
            review_data = content.p
        review = review_data.text
        reviews.append(review)
        name = name_data.text
        rest_names.append(name)
        try:
            address = r.address.text
            address = address.strip()
        except:
            address = 'No address provided'
        rest_addresses.append(address)
        rest_url = 'https://www.yelp.com' + r.a['href']
        rest_html = get_data_using_cache(rest_url)
        page_soup_2 = BeautifulSoup(rest_html, 'html.parser')
    category = page_soup.find_all('span', class_="category-str-list")
    for c in category:
        try:
            rest_category = c.a.text
        except:
            rest_category = 'No type provided'
        rest_types.append(rest_category)


    rest_dict = []
    rest_dict = list(zip(rest_names, rest_types, rest_addresses, rest_state, rest_price, reviews, ratings))
    csv_rest = open(RESTAURANT_CSV, "w")
    writer = csv.writer(csv_rest)
    writer.writerows(rest_dict)
    csv_rest.close()
    insert_data_rest()

    reviews_lst = []
    reviews_lst = list(zip(reviews))
    csv_review = open(REVIEWS_CSV, "w")
    writer = csv.writer(csv_review)
    writer.writerows(reviews_lst)
    # for r in reviews:
    #     csv_review.write("{}\n".format(r))
    csv_review.close()
    insert_data_review()
    return

state_list = ['AK','AL','AR','AS','AZ','CA','CO','CT','DC','DE','FL','GA','GU','HI','IA','ID','IL','IN','KS','KY','LA','MA','MD','ME',
'MI','MN','MO','MP','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','PR','RI','SC', 'SD', 'TN', 'TX', 'UT',
'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']
def populate_db():
    for state in state_list:
        get_yelp_data(state)
    return

def load_help_text():
    with open('help.txt') as f:
        return f.read()

def yelp_interactive_search():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    help_text = load_help_text()
    primary_commands = ['state', 'type', 'help']
    print ("Please enter either 'state' or 'type' to group the data. Enter 'help' for assistance with commands.")
    response = ''
    response = input('Enter a command: ')
    while response != 'exit':
        if len(response.strip().split()) < 1:
            response = input('Enter a command: ')
            continue
        if response.split()[0] not in primary_commands:
            print("Command not recognized: " + response)
            response = input("Enter a command: ")
            continue
        words = response.split()
        if words[0] == 'help':
            print(help_text)
            response = input("Enter a command: ")
            continue
        elif words[0].lower() == 'state':
            ordering = input("Enter 'price' or 'rating' to order the data: ")
            if 'price' in ordering.lower().split():
                statement = "SELECT State, AVG(MaxPrice) FROM Restaurants GROUP BY State ORDER BY AVG(MaxPrice) DESC LIMIT 53"
            elif 'rating' in ordering.lower().split():
                statement = "SELECT State, AVG(StarRatings) FROM Restaurants GROUP BY State ORDER BY AVG(StarRatings) DESC LIMIT 53"
            else:
                while 'price' not in ordering.lower().split() or 'rating' not in ordering.lower().split():
                    ordering = input("Please enter either 'price' or 'rating': ")
                if 'price' in ordering.lower().split():
                    statement = "SELECT State, AVG(MaxPrice) FROM Restaurants GROUP BY State ORDER BY AVG(MaxPrice) DESC LIMIT 53"
                else:
                    statement = "SELECT State, AVG(StarRatings) FROM Restaurants GROUP BY State ORDER BY AVG(StarRatings) DESC LIMIT 53"
            data_yelp = cur.execute(statement).fetchall()
            if data_yelp[0][1] > 5:
                title_add_on = "Average Price via Yelp"
            else:
                title_add_on = "Average Rating via Yelp"

            trace0 = go.Bar(
                x=[z[0] for z in data_yelp],
                y=[z[1] for z in data_yelp],
                marker=dict(
                    color='rgb(158,202,225)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=1.5,
                    )
                ),
                opacity=0.6
            )

            data = [trace0]
            layout = go.Layout(
                title='Restaurants Grouped By State, Ordered By ' + title_add_on,
            )

            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='text-hover-bar')

            response = input("Enter a command: ")
            continue


        elif words[0].lower() == 'type':
            ordering = input("Enter 'price' or 'rating' to order the data: ")
            if 'price' in ordering.lower().split():
                statement = "SELECT Type, AVG(MaxPrice) FROM Restaurants GROUP BY Type ORDER BY AVG(MaxPrice) DESC LIMIT 100"
            elif 'rating' in ordering.lower().split():
                statement = "SELECT Type, AVG(StarRatings) FROM Restaurants GROUP BY Type ORDER BY AVG(StarRatings) DESC LIMIT 100"
            else:
                while 'price' not in ordering.lower().split() or 'rating' not in ordering.lower().split():
                    ordering = input("Please enter either 'price' or 'rating': ")
                if 'price' in ordering.lower().split():
                    statement = "SELECT Type, AVG(MaxPrice) FROM Restaurants GROUP BY Type ORDER BY AVG(MaxPrice) DESC LIMIT 100"
                else:
                    statement = "SELECT Type, AVG(StarRatings) FROM Restaurants GROUP BY Type ORDER BY AVG(StarRatings) DESC LIMIT 100"
            data_yelp = cur.execute(statement).fetchall()
            if data_yelp[0][1] > 5:
                title_add_on = "Price"
            else:
                title_add_on = "Rating"

            trace0 = go.Bar(
                x=[z[0] for z in data_yelp],
                y=[z[1] for z in data_yelp],
                marker=dict(
                    color='rgb(158,202,225)',
                    line=dict(
                        color='rgb(8,48,107)',
                        width=1.5,
                    )
                ),
                opacity=0.6
            )

            data = [trace0]
            layout = go.Layout(
                title='United States Restaurants Grouped By Type, Ordered By ' + title_add_on,
            )

            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='text-hover-bar')

            response = input("Enter a command: ")
            continue
    print("Bye")
    return




#init_database()
#get_yelp_data()
#populate_db()
yelp_interactive_search()
