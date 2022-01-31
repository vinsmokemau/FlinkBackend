"""Company Utils."""

# Finnhub
import finnhub


def is_nyse_symbol(symbol: str) -> bool:
    finnhub_client = finnhub.Client(api_key="c7rku5qad3iel5ubd06g")
    companies = finnhub_client.stock_symbols('US')
    symbols = [company['symbol'] for company in companies]
    return symbol in symbols
