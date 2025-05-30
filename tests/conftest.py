"""Fixtures for the IRM KMI api package."""
from __future__ import annotations

import json
from unittest.mock import MagicMock

from irm_kmi_api import IrmKmiApiClientHa
from irm_kmi_api.const import IRM_KMI_TO_HA_CONDITION_MAP


def load_fixture(fixture):
    with open(f"tests/fixtures/{fixture}", 'rb') as f:
        return f.read()


def get_api_data(fixture: str) -> dict:
    return json.loads(load_fixture(fixture))


def get_api_with_data(fixture: str) -> IrmKmiApiClientHa:
    api = IrmKmiApiClientHa(session=MagicMock(), user_agent='', cdt_map=IRM_KMI_TO_HA_CONDITION_MAP)
    api._api_data = get_api_data(fixture)
    return api

def is_serializable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False

def assert_all_serializable(elements: list):
    for element in elements:
        for v in element.values():
            assert is_serializable(v)