"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import get_standard_tap_tests
from tap_immuta.tap import TapImmuta

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "api_key": "myImmutaApiKey",
    "immuta_host": "https://myinstance.cloud.immuta.com",
}

INTEGRATION_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "api_key": os.environ.get("TAP_IMMUTA_API_KEY"),
    "immuta_host": os.environ.get("TAP_IMMUTA_IMMUTA_HOST"),
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapImmuta, config=INTEGRATION_CONFIG)
    for test in tests:
        test()
