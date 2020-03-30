FROM python:3.6

ADD . /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# RUN python -m spacy download en

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
