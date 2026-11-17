"""API keys from environment variables. See /.env.example at repository root."""

import os

FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
QUANDL_API_KEY = os.environ.get("QUANDL_API_KEY", "")