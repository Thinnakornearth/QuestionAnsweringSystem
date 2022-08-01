FROM python:3.9
# ENV PYTHONBUFFERED 1
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

CMD python api-test.py