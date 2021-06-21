import json
import logging
import requests
import re
import nltk
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from data.config import API_KEY, OMDB_API_URL
from errors.error_handler import ErrorHandler

# Suppress unnecessary SSL certificate warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Util method to check if movie id conforms to valid format and returns boolean value if it matches pattern
def is_movie_id_valid(movie_id):
    regex = re.compile(r"^[t]{2}\d+$")
    if movie_id != '' and len(movie_id) != 9:
        return False
    else:
        return bool(regex.search(movie_id))


class IMDBWebScraper:
    """
    This class is used to encapsulate all attributes and methods which helps with
    web-scraping and thereby returns the movie details from imdb pages like pages lists top rated
    imdb movies and each movie details like Actors, Synopsis(Plot), Director etc.
    """
    def __init__(self, url):
        self.url = url

    # This function uses Beautiful Soup which is web-scraping python library helps in scraping the web pages and
    # returns the html parsed for further processing
    def scrape_webpage(self, url=None):
        url = url if url else self.url
        res = requests.get(url, verify=False)
        parsed_data = BeautifulSoup(res.content, 'html5lib')
        return parsed_data

    # This function returns the top 5(count) imdb movie ids
    def get_movie_ids(self, count):
        if isinstance(count, int):
            if count >= 0:
                try:
                    data = self.scrape_webpage()
                    movies_list = data.body.find("tbody", {"class": "lister-list"})
                    movies_list_items = movies_list.find_all('tr')
                    movie_ids = []

                    for i, chart_row in enumerate(movies_list_items):
                        while i < count:
                            movie_id = chart_row.find("div", {"class": "seen-widget"})['data-titleid']
                            movie_ids.append(movie_id)
                            break
                    return movie_ids

                except Exception as ex:
                    logging.error(ex)
            else:
                ErrorHandler(f'Error: Negative count {count} not allowed').raise_error()
                return ValueError('Negative count not allowed')
        else:
            ErrorHandler(f'Error: count {count} <str> type not allowed').raise_error()
            return TypeError('Only integer type of count allowed')

    # This function returns the synopsis or short summary of each movie
    def get_synopsis(self, movie_id):
        if is_movie_id_valid(movie_id):
            synopsis = ''
            url = f'https://www.imdb.com/title/{movie_id}'
            try:
                data = self.scrape_webpage(url)
                synopsis = data.body.find('div', 'plot_summary').findChild('div', 'summary_text').getText()
            except Exception as ex:
                logging.error(ex)

            if not synopsis:
                logging.error(f"No Synopsis found for movie_id {movie_id}")
            return synopsis
        else:
            ErrorHandler('Invalid movie id, Please try again.').raise_error()

    @staticmethod
    def get_kw_synopsis(synopsis):
        """
        The Python NLTK library contains a default list of stop words.
        To remove stop words, you need to divide your text into tokens (words),
        and then check if each token matches words in your list of stop words.
        If the token matches a stop word, you ignore the token.
        Otherwise you add the token to the list of valid words.
        """
        if isinstance(synopsis, str):
            try:
                # Remove punctuation
                text = re.sub('[^a-zA-Z]', ' ', str(synopsis))

                # Converting synopsis text to lowercase
                text = text.lower()

                # Removing tags
                text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)

                # Removing special characters and digits
                text = re.sub("(\\d|\\W)+", " ", text)

                # Collecting basic set of stop words using nltk package
                stop_words = set(nltk.corpus.stopwords.words('english'))

                # Tokenizing the synopsis using nltk tokenizer
                word_tokens = nltk.tokenize.word_tokenize(text)

                filtered_synopsis = [w for w in word_tokens if not w.lower() in stop_words]
                return filtered_synopsis

            except Exception as ex:
                logging.error(ex)

        else:
            ErrorHandler(f"Invalid synopsis {synopsis}, Please check!").raise_error()
            return Exception(f"Invalid synopsis")

    # This function accepts movie id as an argument and then returns the movie details as json
    @staticmethod
    def get_movie_details(movie_id):
        if is_movie_id_valid(movie_id):
            endpoint = f'{OMDB_API_URL}?i={movie_id}&apiKey={API_KEY}'
            movie_details = requests.get(endpoint)
            # json converted to python dict below
            return json.loads(movie_details.text)
        else:
            ErrorHandler(f"Invalid movie ID {movie_id}").raise_error()
            raise Exception(f"Invalid movie ID")
