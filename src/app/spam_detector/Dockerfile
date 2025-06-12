FROM python:3.12-slim-bullseye

RUN apt-get update \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --requirement /app/requirements.txt

RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

COPY . /app

EXPOSE 8001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
