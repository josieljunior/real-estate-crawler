
FROM python:3.8

WORKDIR /app

COPY /real_estate_crawler/scrapy.cfg .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["tail", "-f", "/dev/null"]
