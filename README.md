# Flights

**Flights** is a web application, backed by the power of [MariaDB ColumnStore](https://mariadb.com/docs/features/mariadb-columnstore/), allows you to analyze millions [flight records from the United States Department of Transportation](https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time) in real time without needing to add any indexes!

<p align="center" spacing="10">
    <kbd>
        <img src="media/demo.gif" />
    </kbd>
</p>

This application is made of two parts:

* Client
    - web UI that communicates with REST endpoints available through an API app (see below).
    - is a React.js project folder.
* API
    - uses the [MariaDB Python Connector](https://github.com/mariadb-corporation/mariadb-connector-python) to connect to MariaDB.
    - is a Python project located int the [api](src/api) folder.

This README will walk you through the steps for getting the `Flights` web application up and running using MariaDB.

# Table of Contents
1. [Requirements](#requirements)
2. [Getting started with MariaDB ColumnStore](#mariadb)
3. [Get the code](#code)
3. [Configure, build and run the app](#app)
    1. [Configure](#configure-api-app)
    2. [Create and activate a Python virtual environment](#activate-virtual-env)
    3. [Install Python packages](#install-python-packages)
    4. [Build and run the Python API app](#build-run-api)
    5. [Build and run the Client app](#build-run-client)
4. [Support and contribution](#support-contribution)
5. [License](#license)

## Requirements <a name="requirements"></a>

This sample application requires the following to be installed/enabled on your machine:

* [Python (v. 3+)](https://www.python.org/downloads/) (development headers must also be installed, e.g. python3-dev for Debian/Ubuntu)
* [MariaDB Connector/C (v. 3.1.5+)](https://mariadb.com/products/skysql/docs/clients/mariadb-connector-c-for-skysql-services/) (used by Connector/Python)
* [Node.js (v. 18+)](https://nodejs.org/en/) (for the Client/UI app)
* [NPM (v. 6+)](https://docs.npmjs.com/) (for the Client/UI app)
* [MariaDB command-line client](https://mariadb.com/products/skysql/docs/clients/mariadb-clients/mariadb-client/) used to connect to MariaDB database instances and used by the `mariadb` Python package

## 1.) Getting Started with MariaDB ColumnStore <a name="mariadb"></a>

[MariaDB](https://mariadb.com) is a community-developed, commercially supported relational database management system, and the database you'll be using for this application.

This sample uses MariaDB ColumnStore. The quickest way to get started is by using the [MariaDB ColumnStore Quickstart Guide](https://github.com/izzthedude/mariadb-columnstore-quickstart), which will walk you through the process of getting a MariaDB database instance (via Docker container) up, running and loaded with the data necessary for this sample app.

**TL;DR** - Check out the [MariaDB ColumnStore Quickstart](https://github.com/izzthedude/mariadb-columnstore-quickstart) before proceeding to the next step.

## 2.) Get the code <a name="code"></a>

First, use [git](git-scm.org) (through CLI or a client) to retrieve the code using `git clone`:

```bash
git clone https://github.com/izzthedude/flights-app-python.git

cd flights-app-python
```

Next, because this repo uses a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules), you will need to pull the [client application](https://github.com/izzthedude/flights-app-client) using:

```bash
git submodule update --init --recursive
```

## 3.) Configure, Build and Run the App <a name="app"></a>

**Important**: Before proceeding you'll need to have a MariaDB ColumnStore instance preloaded with flight data for this application to use. You can find more information [here](#mariadb).

This application is made of two parts:

* Client
    - web UI that communicates with REST endpoints available through an API app (see below).
    - is a React.js project folder.
* API
    - uses the [MariaDB Python Connector](https://github.com/mariadb-corporation/mariadb-connector-python) to connect to MariaDB.
    - is a Python project located int the [api](src/api) folder.

### a.) Configure the app <a name="configure-api-app"></a>

Configure the MariaDB connection by adding an [.env file](https://pypi.org/project/python-dotenv/) to the project within the [api](src/api) folder. Only change the values for `DB_PASS`.

#### Password
The `<password>` is whatever you have set as the password in the MariaDB Docker container. Refer [here](https://github.com/izzthedude/mariadb-columnstore-quickstart) for more information.

Example implementation:

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=app_user
DB_PASS=<password>
DB_NAME=travel
```

The environmental variables from `.env` are used within [src/api/_env.py](src/api/_env.py) for the MariaDB Python Connector connection configuration settings:

```python
config = {
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT")),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'database': os.getenv("DB_NAME")
}
```

#### Host address
If `127.0.0.1` does not work, try running this command:
```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mcs_container
```
This will return an IP address that you can try to use in place of `127.0.0.1`. If it still does not work, Google may or may not help with your issue more than I can lol.

**Configuring .env and tasks.py for the MariaDB cloud database service [SkySQL](https://mariadb.com/products/skysql/)**

Note: MariaDB SkySQL requires SSL additions to connection. Details coming soon!

### b.) Create and activate a Python virtual environment <a name="activate-virtual-env"></a>

A virtual environment is a directory tree which contains Python executable files and other files which indicate that it is a virtual environment. Basically, it's the backbone for running your Python Flask app.

Creation of [virtual environments](https://docs.python.org/3/library/venv.html?ref=hackernoon.com#venv-def) is done by executing the following command (within [/src/api](src/api)):

```bash
cd src/api

python3 -m venv venv
```

**Tip**: Tip: pyvenv is only available in Python 3.4 or later. For older versions please use the [virtualenv](https://virtualenv.pypa.io/en/latest/) tool. 

Before you can start installing or using packages in your virtual environment, you’ll need to activate it. Activating a virtual environment will put the virtual environment-specific python and pip executables into your shell’s PATH.

Activate the virtual environment using the following command (within [/src/api](src/api)):

```bash
./venv/bin/activate
```

### c.) Install Python packages <a name="install-python-packages"></a>

[Flask](https://flask.palletsprojects.com/en/1.1.x/?ref=hackernoon.com) is a micro web framework written in Python. It is classified as a [microframework](https://en.wikipedia.org/wiki/Microframework) because it does not require particular tools or libraries. 

**TL;DR** It's what this app uses for the API.

This app also uses the MariaDB Python Connector to connect to and communicate with MariaDB databases. 

Install the necessary packages by executing the following command:

```bash
pip3 install -r ../../requirements.txt
```

### d.) Build and run the [API app](src/api) <a name="build-run-api"></a>

Once you've pulled down the code and have verified that all of the required packages are installed you're ready to run the application! 

Execute the following CLI command to start the the Python project (within [/src/api](src/api)):

```bash
python3 api.py
```

### e.) Build and run the [UI (Client) app](https://github.com/izzthedude/flights-app-client) <a name="build-run-client"></a>

Once the API project is running you can now communicate with the exposed endpoints directly (via HTTP requests) or with the application UI, which is contained with the `client` folder of this repo.

To start the `client` application follow the instructions [here](https://github.com/izzthedude/flights-app-client).

## Support and Contribution <a name="support-contribution"></a>

This is a fork strictly for personal/academic use. This fork is **NOT** officially affiliated or endorsed by the original developers. As such, any issues from my changes **MUST NOT** be reported to them.


## License <a name="license"></a>
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=plastic)](https://opensource.org/licenses/MIT)

