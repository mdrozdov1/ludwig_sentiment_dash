FROM python:3.6

ADD . /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:app.server"]