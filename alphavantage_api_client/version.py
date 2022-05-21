import subprocess

# version
alphavantage_api_client_version = subprocess.run(['git', 'describe', '--tags'],
                                                 stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

__version__ = alphavantage_api_client_version
