# WebScraper

# Project Summary:
This project develops web scraping techniques to extract imdb movie details and writes the movie data to csv files and then pushes the file to S3 bucket using boto3 client

# Modules
1. IMDBWebscraper - which manages scraping and returning the required imdb data like IDs, synopsis and other details 
2. BucketUtils - It manages CRU operations on S3 bucket like uploading & downloading csv file from S3 bucket, creating bucket etc.
3. MovieDataManager - It perform all write & read operations on csv file before going for bucket operations
4. Main - Entry point of application which summarizes all operations that go through the application flow
5. Tests - Which includes all unit test cases
6. Errors - Which returns errors

# Dependencies for app to run
1. re - regex for some validation
2. requests - for making http requests
3. nltk - language processing for filtering keywords in a given sentence
4. logging - To log errors
5. unittest - Unit test module for assert statements
6. csv - module to read and write csv files
7. json - module to load and parse json
8. Beautiful Soup - Webscraping library

# Commands to run
1. python -m unittest - To run test cases
2. pip install #module_name# - To install dependencies
3. python main.py - To run the application
