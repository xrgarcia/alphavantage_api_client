from python:3.9-slim-buster

WORKDIR /src

ADD app.py ./
ADD ./tests/ ./tests/
ADD pytest.ini ./
ENV ALPHAVANTAGE_API_KEY = ${ALPHAVANTAGE_API_KEY}
RUN python -m pip install --upgrade pip
RUN pip install alphavantage-api-client pytest

CMD ["pytest","-vv", "-raPp", "-k", "test_single_client_integration"]