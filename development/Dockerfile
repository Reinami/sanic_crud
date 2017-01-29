FROM python:3.6
MAINTAINER Ernest Atkinson

ADD . /code
RUN pip3 install --upgrade pip
RUN pip3 install -r /code/requirements.txt

EXPOSE 8000

WORKDIR /code

CMD ["python", "main.py"]