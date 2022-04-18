"""
Apps7 adNetwork ETL Application 
- runs on port 5000
- base endpoint triggers the application workflow
- Workflow:
    - Read input params which are: adNetwork (list), date (list)
    - Collects and parses the data
    - Writes to postgres database, table: daily_report
"""

from flask import Flask, request, jsonify
import requests as r
from datetime import datetime
import pandas as pd
import json
import structlog

APP = Flask(__name__)
LOG = structlog.get_logger()
BASE_ENDPOINT = "https://storage.googleapis.com/expertise-test/"


@APP.route("/SuperNetwork", methods=['POST'])
def super_network_trigger(base_endpoint = BASE_ENDPOINT):
  LOG.info("SuperNetwork trigger called")
  data = request.get_json()
  json_response_data = jsonify(data)
  dict_data = json.loads(data)

  LOG.info(dict_data)
  # iterate through dates
  for date in dict_data["date"]:
    
    # cast date in standard format
    date = date.strftime("%Y-%m-%d")
    
    # call the andpoint
    endpoint = base_endpoint + f"supernetwork/report/daily/{date}.csv"
    req = r.get(endpoint)

    req_list = [[el.strip("\r") for el in line.split(",")] for line in req.text.split("\n")]
    headers = req_list.pop(0)
    df_req = pd.DataFrame(req_list, columns=headers)

    df_req["Revenue"] = df_req.apply(lambda row: row["Revenue"].strip("€"), axis = 1)
    df_req["Currency"] = "EUR"
    df_req["Date"] = pd.to_datetime(df_req["Date"])

    LOG.info(df_req)

  return json_response_data


@APP.route("/AdUmbrella", methods=['POST'])
def super_network_trigger(base_endpoint = BASE_ENDPOINT):
  LOG.info("SuperNetwork trigger called")
  data = request.get_json()
  json_response_data = jsonify(data)
  dict_data = json.loads(data)

  LOG.info(df_req)
  # iterate through dates
  for date in dict_data["date"]:

    # cast date in standard format
    # some new comment
    date = date.strftime("%Y-%m-%d")

    # call the andpoint
    endpoint = base_endpoint + f"reporting/adumbrella/adumbrella-{date.day}_{date.month}_{date.year}.csv"
    req = r.get(endpoint)

    req_list = [[el.strip("\r").rstrip(" (usd)") for el in line.split(",")] for line in req.text.split("\n")]
    headers = req_list.pop(0)
    summary = req_list.pop(-1)
    df_req = pd.DataFrame(req_list, columns=headers)

    df_req["Currency"] = "USD"
    df_req["Date"] = pd.to_datetime(df_req["Date"])

    LOG.info(df_req)
    assert "Total" in summary, "Last row was removed... But it did not contain Totals as per usual."

  return json_response_data

