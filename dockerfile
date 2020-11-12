FROM python:3.6

RUN mkdir -p /app/src
WORKDIR /app/src

COPY reqs.txt ./
RUN pip install --no-cache-dir -r reqs.txt
COPY src .

CMD [ "python3", "./main.py" ]