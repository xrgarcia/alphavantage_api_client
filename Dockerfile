from python:3.10-slim-buster

WORKDIR /

ADD app.py ./src/
ADD ./tests/ ./src/tests/
ENV ALPHAVANTAGE_API_KEY = ${ALPHAVANTAGE_API_KEY}
RUN python -m pip install --upgrade pip
RUN pip install pytest alphavantage_api_client
WORKDIR /src

CMD ["pytest","-vv", "-raPp", "-m", "unit or integration"]