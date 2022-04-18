# Apps7-dev (solution to Problems 1-3)
This repo contains the solution to the problems in the Data engineer expertise test.

## Problem 1: Collecting data in containers
The service is set up with `docker-compose.yaml` and `Docker`.
The `docker compose` is build from two parts:
- __Application__ that collects the data from the endpoints and saves it into the database
- A sample __postgres database__

To run the service simply run `docker compose up` in the root of the repo.

The __application__ was developed in Python with Flask. It is a REST API service that is triggered with the call to the right api endpoint. No authentication is required.
To call the service use localhost address and port 5000 (running locally) `http://127.0.0.1:5000` and the endpoint that is the name of the _adNetwork_.
The headers must include `Content-Type: application/json` with additional information in the body consisting of a list of dates that you want to collect the data for.

### Example:
To collect the data for the adNetwork `adUmbrella` for dates `2017-09-15`, `2017-09-16`:

Create a POST request to: `http://127.0.0.1:5000/AdUmbrella` with header: `{"Content-Type": "application/json"}` and date info in the body: `{"date": ["2017-09-15", "2017-09-16"]}`.
There is a sample script created `call_app.py` that only needs the `request` package and runs for the _adNetworks_ and _dates_ described in the __Problem 1__. That will fill the `daily_report` table with the _adNetworks_ data.

### Event flow
- Call the API endpoint.
- Data collected from the specified urls based on _adNetwork_ and _date_ info and transformed into proper format for the database table
- If the `daily_report` table does not exists it's first created
- The collected data is inserted into the `daily_report` table

### Remarks:
- The reasoning behind endpoint for each adNetwork is that in the description of the problem the application is supposed to be scalable to other adNetwork data. One of the ways to to that is to consider each new adNetwork as a new module/function that can be added with an additional endpoint to be called.
- To call the service for additional adNetworks the only parameter that should be added in the scheduler is the extra api endpoint to the existing api endpoint set.
- Postgres db is used as a "placeholder" database. In practice the database would not "come with" the service. The service would be developed based on the database that would be used.
- For production use the service requires authentication and secrets (e.g. Github secrets, Secret Manager, Key Vault,...) for sensitive information
- The service also requires authentication
- Before deploying into production at least some basic Unit tests must also be added. Preferably testing each component/endpoint of the application (with Python using `pytest` and `mocker`)

## Problem 2: Analyzing data
The answers for Problem 2 and Problem 3 are in `answers.txt`

Analysis of the data performed in Jupyter Notebook: `problem2\Problem 2 - Sanity Check.ipynb`
Packages used: `pandas` and `requests` and `jupyterlab` for jupyter notebooks.

## Problem 3: Reliable design
The answers for Problem 2 and Problem 3 are in `answers.txt`
