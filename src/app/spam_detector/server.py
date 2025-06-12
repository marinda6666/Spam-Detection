from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from utils import preprocess_text, get_prediction, load_model

load_dotenv()

THRESHOLD = 0.90

MODEL_CHECKPOINT = Path('models/log_reg.joblib')
VECTORIZER_CHECKPOINT = Path('models/vec_log_reg.joblib')

app = FastAPI()


model = load_model(MODEL_CHECKPOINT)
vectorizer = load_model(VECTORIZER_CHECKPOINT)


@app.get('/')
def health_check():
    return {'health_check': 'OK'}


@app.get('/get_prediction')
def filter_message(msg: str):
    return {'is_spam': get_prediction(msg, model, vectorizer, return_proba=False)}