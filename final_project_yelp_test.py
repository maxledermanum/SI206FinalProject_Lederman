from final_project_yelp import *
import unittest


class TestDatabase(unittest.TestCase):

    def test_resturants_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM Restaurants'
        results = cur.execute(sql)
        result_lst = results.fetchall()
        self.assertEqual(len(result_lst), 419)


    def test_reviews_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Review FROM Reviews'
        results = cur.execute(sql)
        results_lst = results.fetchall()
        self.assertEqual(len(results_lst), 419)

    def test_first_restaurant_name(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM Restaurants'
        results = cur.execute(sql)
        result_lst = results.fetchone()
        self.assertTrue(result_lst, 'Glacier BrewHouse')

    def test_first_restaurant_state(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql2 = 'SELECT State FROM Restaurants'
        results2 = cur.execute(sql2)
        results_lst2 = results2.fetchone()
        self.assertTrue(results_lst2, 'AK')

    def test_first_restaurant_address(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Address FROM Restaurants'
        results = cur.execute(sql)
        result_lst = results.fetchone()
        self.assertTrue(result_lst, '737 W 5th AveAnchorage, AK 99501')

    def test_first_restaurant_price(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT MaxPrice FROM Restaurants'
        results = cur.execute(sql)
        results_lst = results.fetchall()
        self.assertTrue(results_lst[0], '30')

    def test_first_restaurant_rating(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT StarRatings FROM Restaurants'
        results = cur.execute(sql)
        results_lst = results.fetchall()
        self.assertTrue(results_lst[0], '4.0')

    def test_first_review(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Review FROM Reviews'
        results = cur.execute(sql)
        result_lst = results.fetchone()
        self.assertTrue(result_lst, "'Funny thing about Alaska is although it's where Alaska King crab is caught, it sure is hard to find a good Alaskan King Crab spot!' in 164 review")

    def test_first_review_id(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT ReviewId FROM Reviews'
        results = cur.execute(sql)
        results_lst = results.fetchone()
        self.assertTrue(results_lst, '1')


    def test_rest_column_type(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Type FROM Restaurants'
        results = cur.execute(sql)
        results_lst = results.fetchone()
        self.assertEqual(type(results_lst), tuple)

    def test_review_column_type(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql2 = 'SELECT Review FROM Reviews'
        results2 = cur.execute(sql2)
        results_lst2 = results2.fetchone()
        self.assertEqual(type(results_lst2), tuple)

class TestStorage(unittest.TestCase):
    def test_data_storage(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT * FROM Restaurants'
        results = cur.execute(sql)
        results_lst = cur.fetchall()
        self.assertEqual(len(results_lst[0]), 8)


    def test_data_storage2(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT * FROM Reviews'
        results = cur.execute(sql)
        results_lst = cur.fetchall()
        self.assertEqual(len(results_lst[0]), 3)

    def test_data_storage3(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT Type FROM Restaurants'
        results = cur.execute(sql)
        results_lst = cur.fetchall()
        self.assertTrue(results_lst[0], 'pizza')

    def test_data_storage4(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = 'SELECT ReviewId FROM Reviews'
        results = cur.execute(sql)
        results_lst = cur.fetchall()
        self.assertNotEqual(results_lst[0], '1')

# class TestDataProcessing(unittest.TestCase):
#     def test_scraping(self):
#         list_of_restaurants = get_yelp_data("NY")
#         self.assertEqual(len(list_of_restaurants), 10)


unittest.main()
