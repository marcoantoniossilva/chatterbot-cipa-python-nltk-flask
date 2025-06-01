import nltk
import subprocess
import sys

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('floresta')

# Download do modelo do spaCy (pt_core_news_sm)
try:
    import spacy
    spacy.load("pt_core_news_sm")
except (OSError, ImportError):
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "pt_core_news_sm"])