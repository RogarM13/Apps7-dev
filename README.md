# Apps7-dev (solution to the Problems 1-3)
This repo contains the solution to the problems for the Apps7 problem.

## Problem 1: Collecting data in containers
The service is set up with `docker-compose.yaml` and `Docker`.
The `docker compose` is build from two parts:
- __Application__ developed to collect the data from the endpoints and save it into the database
- A sample __postgres database__
To run the service simply run `docker compose up` in the root of the repo.

The __application__ was developed in Python with Flask. It is a REST API service that is triggered with the call to the right api endpoint. Currently no other authentication is needed.
To call the service use localhost address and port 5000 (running locally) `http://127.0.0.1:5000` and the endpoint that is the name of the _adNetwork_.
The headers must include `Content-Type: application/json` with additional information in the body consisting of a list of dates that you want to collect the data for.

##### Example:
To collect the data for the adNetwork `adUmbrella` for dates `2017-09-15`, `2017-09-16`:

Create a POST request to: `http://127.0.0.1:5000/AdUmbrella` with header: `{"Content-Type": "application/json"}` and date info in the body: `{"date": ["2017-09-15", "2017-09-16"]}`.
There is a sample script created called `call_app.py` that only needs the `request` package and runs for the _adNetworks_ and _dates_ described in the __Problem 1__.

##### Event flow
- Call the API endpoint.
- Data is collected from the specified urls based on _adNetwork_ and _date_ info and transformed into proper format for the database table
- If the `daily_report` table does not exists it's first created
- The collected data is inserted into the database

##### Remarks:
- The reasoning behind endpoint for each adNetwork is that in the description the application should be scalable to other adNetwork data. One of the ways to to that is to consider each new adNetwork as a new module/function that can be added.
- Postgres db is used as a "placeholder" database. In practice the database would not "come with" the service. The service would be developed based on the database that would be used.
- For production use the service requires authentication and secrets (e.g. Github secrets, Cloud Key Management, Key Vault,...) for sensitive information
