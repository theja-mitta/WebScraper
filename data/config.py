from pathlib import Path

PROJECT_ROOT_PATH = Path(__file__).parent.parent
DATA_DIRECTORY_PATH = Path(__file__).parent


# AWS S3 credentials
BUCKET_NAME = 'vemitta-datascrape'
FILE_NAME = 'movies.csv'

LOCAL_FILE_NAME = 'current.csv'
LOCAL_FILE_PATH = DATA_DIRECTORY_PATH / 'current'
BUFFER_FILE_NAME = 'movies.csv'
BUFFER_FILE_PATH = DATA_DIRECTORY_PATH / 'buffer'
MOVIES_COUNT = 5
IMDB_URL = 'https://www.imdb.com/chart/top/'

API_KEY = 'fa6a271'
OMDB_API_URL = 'http://www.omdbapi.com/'

CSV_HEADER_FIELDS = ['Title', 'Genre', 'Actors', 'imdbID', 'Keywords']


