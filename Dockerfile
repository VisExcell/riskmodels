FROM python:2.7-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
EXPOSE 5000
CMD ["gunicorn", "--workers=4", "-b 0.0.0.0:5000","wsgi:app"]
