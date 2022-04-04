FROM python:3.9

WORKDIR /app

COPY requirements.txt /

RUN pip install --upgrade pip

RUN pip install python-dev-tools

RUN pip3 install -r /requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "rock_n_blok.wsgi:application", "--bind", "0:8000" ]
