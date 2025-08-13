from edgar import Edgar
from helpers import EDGAR_BASE_URL, fetch_latest_filing, validate_cik

user_agent = 'ABC'
cik = validate_cik('0001045810')
with Edgar(user_agent) as edgar:
    response = edgar.get_submissions(cik)
    name = response.get('name', None)
    tickers = response.get('tickers', None)
    recent_filings = response['filings']['recent']
    latest_date, url = fetch_latest_filing(cik, recent_filings)

print(f'Name: {name} Tickers: {tickers} Latest Filing: {latest_date}\n'
      f'Filing URL: {url}')
