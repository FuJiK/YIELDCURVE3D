"""Environment-based API configuration (no secrets in git)."""

from __future__ import annotations

import os

import quandl


def _load(name: str) -> str:
    return os.environ.get(name, "").strip()


QUANDL_API_KEY: str = _load("QUANDL_API_KEY")
FRED_API_KEY: str = _load("FRED_API_KEY")


def configure_quandl() -> None:
    """Apply Nasdaq Data Link / Quandl API key when set."""
    if QUANDL_API_KEY:
        quandl.ApiConfig.api_key = QUANDL_API_KEY


def require_quandl_key() -> str:
    key = QUANDL_API_KEY
    if not key:
        raise RuntimeError(
            "QUANDL_API_KEY is not set. Copy .env.example to .env or export the variable."
        )
    configure_quandl()
    return key


def require_fred_key() -> str:
    key = FRED_API_KEY
    if not key:
        raise RuntimeError(
            "FRED_API_KEY is not set. Copy .env.example to .env or export the variable."
        )
    return key