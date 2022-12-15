# syntax=docker/dockerfile:1
FROM python:3.9-slim
RUN apt-get update
RUN apt-get install nano
RUN pip install --upgrade pip

RUN mkdir wd
WORKDIR wd

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./

EXPOSE 8080
CMD ["python", "app.py"]

# CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]