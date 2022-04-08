FROM python:3.9-slim-buster

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN pip3 install pytest==7.0.1

COPY . /app


CMD ["python3", "-m", "pytest"]