FROM python

WORKDIR /nn

COPY src /nn/src
COPY requirements.txt /nn

RUN pip install -r requirements.txt
