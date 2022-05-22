import os.path
import pathlib
import subprocess

import setuptools
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# get module version from git tag
client_version = subprocess.run(['git', 'describe', '--tags'],
                             stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
# The text of the README file
README = (HERE / "README.md").read_text()

# assert "." in alphavantage_api_client_version
# assert os.path.isfile("alphavantage_api_client/version.py")
# with open("alphavantage_api_client/VERSION","w", encoding="utf-8") as fh:
#    fh.write(f'{alphavantage_api_client_version}\n')

# This call to setup() does all the work
setup(
    name="alphavantage-api-client",
    version=client_version,
    description="Interact with Alphavantage REST API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/xrgarcia/alphavantage-api-client",
    author="Slashbin, LLC",
    author_email="support@slashbin.us",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    py_modules=["alphavantage_api_client"],
    package_dir={'':'src'},
    include_package_data=True,
    install_requires=["requests"],
    python_requires=">=3.6"
)
