"""Company Utils."""

# Django
from django.conf import settings

# Utilities
import finnhub


def is_nyse_symbol(symbol: str) -> bool:
    """
    Function that make a request to Finnhub API to get all the NYSE symbols.
    """
    finnhub_client = finnhub.Client(api_key=settings.FINNHUB_APIKEY)
    companies = finnhub_client.stock_symbols('US')
    symbols = [company['symbol'] for company in companies]
    return symbol in symbols
