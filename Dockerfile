FROM python:3.6.0b3
ADD . /application
WORKDIR /application
RUN pip install -r requirements.txt
CMD ["python",  "./run.py" ]