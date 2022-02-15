FROM python:3-alpine

LABEL maintainer="Sahbi Chaieb <sahbi.chaieb@sas.com>"
LABEL description="A container for Unit test"

USER root

RUN pip install --upgrade pip; \
    pip install pandas==1.4.0 \
                scikit-learn==1.0.2; \
    pip install pytest;
    

WORKDIR /home/unittest

COPY . .
