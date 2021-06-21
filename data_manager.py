import csv


# Reads and Writes data to CSV files
import logging


class MovieDataManager:
    def __init__(self, csv_file):
        self.filename = csv_file
        self.file_handler = None

    def _open(self, mode='r'):
        try:
            file_handler = open(self.filename, mode, newline='')
            self.file_handler = file_handler
            return file_handler
        except IOError as e:
            err, strerror = e.args
            print(f"I/O error({err}): {strerror}")
        except FileNotFoundError as ex:
            print(f"Oops! File {self.filename} not found - {str(ex)}")
        except Exception as ex:
            print(f"Error while opening file {self.filename} - {str(ex)}")

    def _close(self):
        if self.file_handler:
            self.file_handler.close()

    def copyfile(self, destination_path):
        fh = self._open()
        with open(destination_path, 'w') as new_file:
            new_file.write(fh.read())
        self._close()

    def get_movie_ids(self, count=None):
        movie_ids = []
        fh = self._open()
        content = csv.DictReader(fh)
        for line, row in enumerate(content):
            if row:
                movie_ids.append(row["imdbID"])
                if count and count == line:
                    break
        self._close()
        return movie_ids

    def append_to_csv(self, data):
        # data = {id1: {'details': <dict>, 'synopsis': <list>}, id2: {....}, id3: {....}}
        fh = self._open(mode='a')
        for movie_id, movie_data in data.items():
            row = [movie_data['details']['Title'],
                   movie_data['details']['Genre'],
                   movie_data['details']['Actors'],
                   movie_id,
                   movie_data['synopsis']]
            writer = csv.writer(fh)
            writer.writerow(row)
        self._close()

    def fetch_movie_details_with_key(self, key):
        # check if csv from s3 is already present in current folder
        # read csv and find for actors/genre match then return the matched rows
        if isinstance(key, str):
            fh = self._open(mode='r')
            for row in fh:
                if key in row:
                    return row
            self._close()
        else:
            logging.error('Please pass the valid key type <str>')
            return 'Please pass the valid key'
