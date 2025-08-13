from pyrate_limiter import Duration, Limiter, Rate
from urllib3.util.retry import Retry

BASE_URL = 'https://data.sec.gov'
EDGAR_BASE_URL = 'https://www.sec.gov/Archives/edgar/data/'
XBRL = f'{BASE_URL}/api/xbrl'
SUBMISSIONS = f'{BASE_URL}/submissions'
COMPANY_CONCEPTS = f'{XBRL}/companyconcept'
COMPANY_FACTS = f'{XBRL}/companyfacts'
FRAMES = f'{XBRL}/frames'
MAX_REQUESTS_PER_SECOND = 10
MAX_RETRIES = 3
BACKOFF_FACTOR = 1 / MAX_REQUESTS_PER_SECOND
SEC_THROTTLE_LIMIT_RATE = Rate(MAX_REQUESTS_PER_SECOND, Duration.SECOND)
limiter = Limiter(
    SEC_THROTTLE_LIMIT_RATE,
    raise_when_fail=True,
    max_delay=60_000
).as_decorator()


def fetch_latest_filing(cik: str, filings: dict) -> tuple[str, str]:
    accession_no = filings['accessionNumber'][0]
    latest_date = filings['filingDate'][0]
    primary_doc = filings['primaryDocument'][0]
    url = f'{EDGAR_BASE_URL}/{cik}/{accession_no}/{primary_doc}'
    
    return latest_date, url 


def is_cik(cik: str) -> bool:
    try:
        int(cik)
        return 1 <= len(cik) <= 10
    except ValueError:
        return False


def limiter_mapping(*args):
    return 'sec_edgar_api_rate_limit', 1


def validate_cik(cik: str) -> str:
    cik = str(cik).strip().zfill(10)
    if not is_cik(cik):
        raise ValueError('CIK is not valid.')

    return cik


retries = Retry(
    total=MAX_RETRIES,
    backoff_factor=BACKOFF_FACTOR,
    status_forcelist=[408, 425, 429, 500, 502, 503, 504],
)

class EdgarError(Exception):
    pass
