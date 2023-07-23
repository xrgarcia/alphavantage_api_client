docker build --tag alphavantage-end-to-end-test .
docker run --env-file ./env_file alphavantage-end-to-end-test
