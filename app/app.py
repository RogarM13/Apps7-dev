"""
Apps7 adNetwork ETL Application
- runs on port 5000
- base endpoint triggers the application workflow
- Workflow:
    - Read input params which are: adNetwork (list), date (list)
    - Collects and parses the data
    - Writes to postgres database, table: daily_report
"""

import json
from datetime import datetime

import pandas as pd
import requests as r
import structlog
from flask import Flask, jsonify, request
from postgres import create_table, insert_data_from_dataframe

APP = Flask(__name__)
LOG = structlog.get_logger()
BASE_ENDPOINT = "https://storage.googleapis.com/expertise-test/"


@APP.route("/SuperNetwork", methods=["POST"])
def super_network_trigger(base_endpoint=BASE_ENDPOINT):
    LOG.info("SuperNetwork trigger called")
    data = request.get_json()
    json_response_data = jsonify(data)
    dict_data = json.loads(data)

    LOG.info(dict_data)
    # iterate through dates
    for date in dict_data["date"]:

        # cast date in standard format
        date = datetime.strptime(date, "%Y-%m-%d")
        date = date.strftime("%Y-%m-%d")

        # call the andpoint
        endpoint = base_endpoint + f"supernetwork/report/daily/{date}.csv"
        req = r.get(endpoint)

        req_list = [
            [el.strip("\r") for el in line.split(",")] for line in req.text.split("\n")
        ]
        headers = req_list.pop(0)
        df_req = pd.DataFrame(req_list, columns=headers)

        df_req["Revenue"] = df_req.apply(lambda row: row["Revenue"].strip("€"), axis=1)
        df_req["Currency"] = "EUR"
        df_req["Date"] = pd.to_datetime(df_req["Date"])

        LOG.info(df_req)

        # always try to first create the table if not exists
        tablecreate = create_table("daily_report")
        LOG.info(tablecreate)

        # data insert
        datainsert = insert_data_from_dataframe(df_req, "daily_report")
        LOG.info(datainsert)

    return json_response_data


@APP.route("/AdUmbrella", methods=["POST"])
def ad_umbrella_trigger(base_endpoint=BASE_ENDPOINT):
    LOG.info("AdUmbrella trigger called")
    data = request.get_json()
    json_response_data = jsonify(data)
    dict_data = json.loads(data)

    LOG.info(dict_data)
    # iterate through dates
    for date in dict_data["date"]:

        # cast date in standard format
        date = datetime.strptime(date, "%Y-%m-%d")

        # call the andpoint
        endpoint = (
            base_endpoint
            + f"reporting/adumbrella/adumbrella-{date.day}_{date.month}_{date.year}.csv"
        )
        req = r.get(endpoint)

        req_list = [
            [el.strip("\r") for el in line.split(",")] for line in req.text.split("\n")
        ]
        headers = req_list.pop(0)

        # check if totals in the last row of the table:
        if "Totals" in req_list[-1]:
            req_list.pop(-1)
            LOG.warning("Last row was removed... It contained summary information.")

        df_req = pd.DataFrame(req_list, columns=headers)
        df_req = df_req.rename(columns={"Revenue (usd)": "Revenue"})
        df_req["Currency"] = "USD"
        df_req["Date"] = pd.to_datetime(df_req["Date"])

        LOG.info(df_req)

        # always try to first create the table if not exists
        tablecreate = create_table("daily_report")
        LOG.info(tablecreate)

        # data insert
        datainsert = insert_data_from_dataframe(df_req, "daily_report")
        LOG.info(datainsert)

    return json_response_data


if __name__ == "__main__":
    from waitress import serve

    serve(APP, host="0.0.0.0", port=5000)
