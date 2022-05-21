import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="alphavantage-api-client",
    version="0.0.1",
    description="Interact with Alphavantage REST API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/xrgarcia/alphavantage-api-client",
    author="Ray Garcia",
    author_email="ray@slashbin.us",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["alphavantage_api_client"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "alphavantageapiclient=__main__:main",
        ]
    },
)