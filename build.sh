rm -rf ./alphavantage_api_client.egg-info
rm -rf ./build
rm -rf ./dist
#pip wheel . -w dist
python3 setup.py bdist_wheel
python3 setup.py sdist
#python3 -m build