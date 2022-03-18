import pytest
import json
import requests

from reset import mdm

good_json = json.loads(
    """
{"count":1,"next":null,"previous":null,"results":[{"id":100000,"name":"Pytest","is_blocked":false,"status":"active","create_date":"2019-12-09T08:12:59.179722Z","update_date":"2021-05-06T09:19:23.780260Z","billing_package_info":{"data_exports_enabled":true,"api_access_tokens_enabled":true,"action_tokens_enabled":true,"max_devices":0,"max_fleets":0,"max_profiles":0,"max_applications":0,"advanced_location_enabled":false,"audit_log_days_ago":90,"app_config_enabled":true,"ota_policy_enabled":true,"force_devices_auth_enabled":false,"remote_access_enabled":false,"famoco_branded_apps_enabled":true,"geofence_enabled":false,"external_provisioning_toggle_enabled":false},"devices_count":17,"ota_labels":["generic"]}]}
"""
)

bad_json = json.loads(
    """
{"errors":{"detail":"Invalid token header. No credentials provided."}}
"""
)


def test_token_is_valid_with_good_token(requests_mock):
    requests_mock.get(
        "https://my.famoco.com/api/organizations/", json=good_json, status_code=200
    )
    assert good_json == requests.get("https://my.famoco.com/api/organizations/").json()
    assert mdm.token_is_valid("good_token") == True


def test_token_is_valid_with_bad_token(requests_mock):
    requests_mock.get(
        "https://my.famoco.com/api/organizations/", json=bad_json, status_code=401
    )
    assert bad_json == requests.get("https://my.famoco.com/api/organizations/").json()
    assert mdm.token_is_valid("bad_token") == False
