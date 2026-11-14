"""API keys from environment variables. See /.env.example at repository root."""

import os

QUANDL_API_KEY = os.environ.get("QUANDL_API_KEY", "")
FRED_API_KEY = os.environ.get("FRED_API_KEY", "")