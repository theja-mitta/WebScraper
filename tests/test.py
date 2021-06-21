import unittest
import requests

from data.config import LOCAL_FILE_PATH, LOCAL_FILE_NAME, FILE_NAME, BUFFER_FILE_PATH, BUFFER_FILE_NAME
from webscraper import IMDBWebScraper
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bucket_utils import *
from data_manager import MovieDataManager

# Suppress unnecessary SSL certificate warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class TestWebscraper(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
    url = 'https://www.imdb.com/chart/top/'
    imdb = IMDBWebScraper(url)  # instantiate the Webscraper Class

    def test_get_movie_ids(self):
        # test case function to check the IMDBWebScraper.get_movie_ids function (Milestone 1)
        """
        Any method which starts with ``test_`` will considered as a test case.
        """
        test_count = 5
        result = self.imdb.get_movie_ids(test_count)
        self.assertEqual(result, ['tt0111161', 'tt0068646', 'tt0071562', 'tt0468569', 'tt0050083'])

        test_count_invalid_str = 'udjbewewj'
        result1 = self.imdb.get_movie_ids(test_count_invalid_str)
        self.assertIsInstance(result1, TypeError)

        test_count_negative_num = -10
        result2 = self.imdb.get_movie_ids(test_count_negative_num)
        self.assertIsInstance(result2, ValueError)

    def test_get_synopsis(self):
        # test case function to check the IMDBWebScraper.get_synopsis function (Milestone 2)
        test_movie_id = 'tt0068646'
        result = self.imdb.get_synopsis(test_movie_id).strip()
        self.assertEqual(result, "An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.")

    def test_get_stop_words(self):
        # test case function to check the IMDBWebScraper.get_kw_synopsis function (Milestone 3)
        test_synopsis = "An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son."
        result = self.imdb.get_kw_synopsis(test_synopsis)
        self.assertEqual(result, ['organized', 'crime', 'dynasty', 'aging', 'patriarch', 'transfers', 'control', 'clandestine', 'empire', 'reluctant', 'son'])

        test_synopsis_invalid = 11111
        result1 = self.imdb.get_kw_synopsis(test_synopsis_invalid)
        self.assertIsInstance(result1, Exception)

    def test_get_movie_details(self):
        # test case function to check the IMDBWebScraper.get_movie_details function (Milestone 4)
        test_movie_id = 'tt0068646'
        result = self.imdb.get_movie_details(test_movie_id)
        self.assertIsInstance(result, dict)

        test_movie_id_invalid = 'jcebckenwenwefoiwe'
        result1 = self.imdb.get_movie_ids(test_movie_id_invalid)
        self.assertIsInstance(result1, Exception)


# Testcases for checking bucket operations in bucket_utils file
class TestBucketUtils(unittest.TestCase):
    bucket = 'vemitta-datascrape'
    filename = FILE_NAME
    object_name = FILE_NAME
    local_filename = str(LOCAL_FILE_PATH/LOCAL_FILE_NAME)
    buffer_filename = str(BUFFER_FILE_PATH / BUFFER_FILE_NAME)

    def test_create_bucket(self):
        # test case function to check if bucket is created with provided name (Milestone 8)
        expr = True if create_bucket(self.bucket) else False
        self.assertTrue(expr)

    def test_upload_csv_file(self):
        # test case function to check if csv file can be uploaded to bucket (Milestone 8)
        expr = True if upload_csv_file(self.buffer_filename, self.bucket, self.object_name) else False
        self.assertTrue(expr)

    def test_download_csv_file(self):
        # test case function to check if csv file can be downloaded from bucket (Milestone 8)
        expr = True if download_csv_file(self.bucket, self.filename, self.local_filename) else False
        self.assertTrue(expr)


# Testcases for checking bucket operations in bucket_utils file
class TestDataManager(unittest.TestCase):

    data_manager = MovieDataManager(str(LOCAL_FILE_PATH / LOCAL_FILE_NAME))  # instantiate the MovieDataManager Class

    def test_fetch_movie_details_with_key(self):
        # Test case for checking if movie details are being fetched based on key like Actors/Genre
        test_key = 'Morgan Freeman'
        result1 = self.data_manager.fetch_movie_details_with_key(test_key)
        self.assertIsInstance(result1, str)

        test_key_1 = 222  # invalid key
        result2 = self.data_manager.fetch_movie_details_with_key(test_key_1)
        self.assertEqual(result2, 'Please pass the valid key')


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
