FROM python:3

WORKDIR /usr/src/app
RUN pip install --force-reinstall pdfminer.six==20221105
