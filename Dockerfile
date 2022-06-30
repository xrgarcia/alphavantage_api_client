from python:3.10-slim-buster

WORKDIR /src

ADD app.py ./
ADD ./tests/ ./tests/
ADD pytest.ini ./
ENV ALPHAVANTAGE_API_KEY = ${ALPHAVANTAGE_API_KEY}
RUN python -m pip install --upgrade pip
RUN pip install pytest alphavantage_api_client

CMD ["pytest","-vv", "-raPp", "-m", "unit or integration"]