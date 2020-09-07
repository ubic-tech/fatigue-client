FROM python:3.8

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install -r /usr/src/app/requirements.txt

EXPOSE 9090

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090"]

# sudo docker run -e AGGR_NAME=<> -p <9090>:9090 --rm aggr
# curl http://127.0.0.1:<9090>/v1/health