from nltk import SnowballStemmer
from typing import Any
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pathlib import Path
import joblib
import re


STOPWORDS = set(stopwords.words('english'))
THRESHOLD = 0.90


def preprocess_text(text: str) -> str:
    stemmer = SnowballStemmer("english")
    clean_text = re.sub(r'[^\w\s]', '', text)
    clean_text = ' '.join([stemmer.stem(x) for x in clean_text.lower().split() if x not in STOPWORDS]) 
    return clean_text

def get_prediction(message: str,
                   model: Any,
                   vectorizer: CountVectorizer | TfidfVectorizer,
                   threshold: int = THRESHOLD,
                   return_proba: bool = False) -> int | float:
    
    processed_msg = vectorizer.transform([preprocess_text(message)])
    probs = model.predict_proba(processed_msg)
    
    if hasattr(model, 'predict_proba') and return_proba:
        return probs
    else:
        return int(probs[0][1] > threshold)
    
def load_model(filename: str | Path) -> Any:
    return joblib.load(filename)


