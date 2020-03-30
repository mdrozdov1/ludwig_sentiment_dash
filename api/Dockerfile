FROM python:3.7

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python -m spacy download en

EXPOSE 3000
