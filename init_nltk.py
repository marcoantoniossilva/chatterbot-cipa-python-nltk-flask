import nltk
import subprocess
import sys

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('floresta')

# Download do modelo do spaCy (en_core_news_sm)
try:
    import spacy
    spacy.load("en_core_news_sm")
except (OSError, ImportError):
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_news_sm"])