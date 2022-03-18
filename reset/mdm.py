import json
import requests

from django.core.exceptions import PermissionDenied
from django.http import Http404

URL_BASE = "https://my.famoco.com/api/organizations/"
URL_DEVICES = URL_BASE + "{}/devices/?famoco_id={}"
URL_RESET = URL_BASE + "{}/devices/{}/reset_cert/"


def token_is_valid(token: str):
    response_orgs = requests.get(
        URL_BASE,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    if response_orgs.status_code == 200:
        return True
    else:
        return False


def get_org(token: str):
    response = requests.get(
        URL_BASE,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    json_data = json.loads(response.content)
    org = {
        "id": json_data["results"][0]["id"],
        "name": json_data["results"][0]["name"],
    }
    return org


def get_devices_with_cert(token: str, org_id: str, device_filter: str = ""):
    response = requests.get(
        URL_DEVICES.format(org_id, device_filter),
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    if response.status_code != 200:
        raise PermissionDenied("token doesn't have required permissions")
    json_data = json.loads(response.content)
    dev_list = json_data.get("results", None)
    try:
        dev_with_cert = [dev for dev in dev_list if dev["cert_registered"]]
    except KeyError:
        raise PermissionDenied
    return dev_with_cert


def reset_cert(token: str, famoco_id: str) -> int:
    org_id = get_org(token)["id"]
    response = requests.put(
        URL_RESET.format(org_id, famoco_id),
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    if response.status_code == 404:
        raise Http404("device not found")
    return response.status_code
