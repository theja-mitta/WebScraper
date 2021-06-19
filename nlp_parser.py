import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')


def synopsis_parser(synopsis):
    # Remove punctuation
    text = re.sub('[^a-zA-Z]', ' ', str(synopsis))

    # Converting synopsis text to lowercase
    text = text.lower()

    # Removing tags
    text = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ", text)

    # Removing special characters and digits
    text = re.sub("(\\d|\\W)+"," ", text)

    # Collecting basic set of stop words using nltk package
    stop_words = set(stopwords.words('english'))

    # Tokenizing the synopsis using nltk tokenizer
    word_tokens = word_tokenize(text)

    filtered_synopsis = [w for w in word_tokens if not w.lower() in stop_words]
    return filtered_synopsis

