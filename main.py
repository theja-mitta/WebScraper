from pathlib import Path
import csv
import logging

from bucket_utils import get_file_from_s3, push_file_to_s3
from data.config import BUCKET_NAME, FILE_NAME, LOCAL_FILE_PATH, LOCAL_FILE_NAME, MOVIES_COUNT, IMDB_URL, \
    BUFFER_FILE_PATH, BUFFER_FILE_NAME, CSV_HEADER_FIELDS
from webscraper import IMDBWebScraper
from data_manager import MovieDataManager


def main():
    # get current CSV from S3 and write to data/current/current.csv
    if Path(LOCAL_FILE_PATH / LOCAL_FILE_NAME).exists():
        Path(LOCAL_FILE_PATH / LOCAL_FILE_NAME).unlink(missing_ok=True)
    get_file_from_s3(BUCKET_NAME, FILE_NAME, str(LOCAL_FILE_PATH/LOCAL_FILE_NAME))

    # get current IMDB movies and write to data/buffer/movies.csv
    imdb = IMDBWebScraper(IMDB_URL)
    current_movie_ids = imdb.get_movie_ids(MOVIES_COUNT)

    # compare IMDB IDs. If stale, start pooling data into movies.csv to start the process. Else, return.
    if not Path(LOCAL_FILE_PATH/LOCAL_FILE_NAME).exists():
        with open(str(LOCAL_FILE_PATH/LOCAL_FILE_NAME), 'w') as file:
            fields = CSV_HEADER_FIELDS
            wt = csv.writer(file)
            wt.writerow(fields)

    s3_data = MovieDataManager(str(LOCAL_FILE_PATH/LOCAL_FILE_NAME))
    existing_ids = s3_data.get_movie_ids()

    data_diff = set(current_movie_ids) - set(existing_ids)
    if not data_diff:
        print(f"Current file data holds good!")

        # Get movie details from csv by passing Genre/Actor as key
        current_data = MovieDataManager(str(LOCAL_FILE_PATH / LOCAL_FILE_NAME))
        print(current_data.fetch_movie_details_with_key('Morgan Freeman'))
    else:
        # Copy the existing s3 data to buffer
        s3_data.copyfile(str(BUFFER_FILE_PATH / BUFFER_FILE_NAME))

        # Append new data to the buffer
        buffer_data = MovieDataManager(str(BUFFER_FILE_PATH / BUFFER_FILE_NAME))

        # new_data = {id1: {'details': <dict>, 'synopsis': <list>}, id2: {....}, id3: {....}}
        new_data = {}
        for imdb_id in data_diff:
            syn = imdb.get_synopsis(imdb_id)
            kw = imdb.get_kw_synopsis(syn)
            details = imdb.get_movie_details(imdb_id)
            details = {k: v for k, v in details.items() if k in ['Title', 'Genre', 'Actors']}

            new_data[imdb_id] = {'details': details, 'synopsis': kw}

        buffer_data.append_to_csv(new_data)

        # Pushing updated csv file to s3 bucket
        if push_file_to_s3(str(BUFFER_FILE_PATH / BUFFER_FILE_NAME), BUCKET_NAME, FILE_NAME):
            print(f"New version of csv file is uploaded to bucket {BUCKET_NAME} successfully")


if __name__ == '__main__':
    main()
