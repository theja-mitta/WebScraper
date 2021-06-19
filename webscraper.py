import json
import requests
import re
import nltk
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from data.config import API_KEY, OMDB_API_URL

# Suppress unnecessary SSL certificate warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def is_movie_id_valid(movie_id):
    regex = re.compile(r"^[t]{2}\d+$")
    if movie_id != '' and len(movie_id) != 9:
        return False
    else:
        return bool(regex.search(movie_id))


class IMDBWebScraper:
    def __init__(self, url):
        self.url = url

    def scrape_webpage(self, url=None):
        url = url if url else self.url
        res = requests.get(url, verify=False)
        parsed_data = BeautifulSoup(res.content, 'html5lib')
        return parsed_data

    def get_movie_ids(self, count):
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
            print(ex)

    def get_synopsis(self, movie_id):
        synopsis = ''
        url = f'https://www.imdb.com/title/{movie_id}'
        try:
            data = self.scrape_webpage(url)
            synopsis = data.body.find('div', 'plot_summary').findChild('div', 'summary_text').getText()
        except Exception as ex:
            print(ex)

        if not synopsis:
            print(f"No Synopsis found for movie_id {movie_id}")
        return synopsis

    @staticmethod
    def get_kw_synopsis(synopsis):
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

    @staticmethod
    def get_movie_details(movie_id):
        if is_movie_id_valid(movie_id):
            endpoint = f'{OMDB_API_URL}?i={movie_id}&apiKey={API_KEY}'
            movie_details = requests.get(endpoint)
            # json converted to python dict below
            return json.loads(movie_details.text)
        else:
            print(f"Invalid movie ID {movie_id}")
            raise Exception(f"Invalid movie id")
