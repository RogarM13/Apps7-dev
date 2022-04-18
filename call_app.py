"""
A simple script that triggers the app and populates the postgres "daily_report" table
"""

import requests as r

date_data = """
{
    "date": ["2017-09-15", "2017-09-16"]
}
"""
header = {"Content-Type": "application/json"}

super_network_response = r.post(
    "http://127.0.0.1:5000/SuperNetwork", headers=header, json=date_data
)
print(super_network_response.text)

ad_umbrella_response = r.post(
    "http://127.0.0.1:5000/AdUmbrella", headers=header, json=date_data
)
print(super_network_response.text)

print("Table populated.")
