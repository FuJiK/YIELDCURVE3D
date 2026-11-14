"""Shared secret loading for local runs and CI."""

from credential.env import FRED_API_KEY, QUANDL_API_KEY, configure_quandl

__all__ = ["FRED_API_KEY", "QUANDL_API_KEY", "configure_quandl"]