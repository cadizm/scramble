FROM python:2

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements/base.txt

CMD [ "python", "bin/runserver.py" ]
