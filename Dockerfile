FROM python:2-slim

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements/base.txt

EXPOSE 9002

CMD ["gunicorn", "--config", "scramble/gunicorn_config.py", "scramble.wsgi:app"]
