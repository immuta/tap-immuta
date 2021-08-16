"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import get_standard_tap_tests
from tap_immuta.tap import TapImmuta

SAMPLE_CONFIG = {
    "api_key": "myImmutaApiKey",
    "hostname": "https://myinstance.cloud.immuta.com",
}

INTEGRATION_CONFIG = {
    "api_key": os.environ.get("TAP_IMMUTA_API_KEY"),
    "hostname": os.environ.get("TAP_IMMUTA_HOSTNAME"),
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapImmuta, config=INTEGRATION_CONFIG)
    for test in tests:
        test()
