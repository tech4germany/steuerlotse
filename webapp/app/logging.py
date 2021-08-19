import logging
from logging.config import dictConfig
import json
import os

from flask import has_request_context, request


def configure_logging():
    with open(os.path.join(os.path.dirname(__file__), '..', 'logging.json')) as f:
        dictConfig(json.load(f))


class AddRequestIdFilter(logging.Filter):
    """Add the request ID to the log (if present)."""

    def filter(self, record):
        if has_request_context() and 'X-Request-ID' in request.headers:
            record.request_id = request.headers['X-Request-ID']

        return True
