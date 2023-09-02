FROM python:3 AS hdt

RUN apt-get update -y && apt-get install -y build-essential

WORKDIR /humanDigitalTwin
COPY ./requirements.txt .
COPY . .

RUN pip install -r requirements.txt
RUN pip install -e ./stereotypes
