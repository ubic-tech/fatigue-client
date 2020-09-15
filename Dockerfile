FROM python:3.7

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install -r /usr/src/app/requirements.txt


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9090"]