from requests import Session
from requests.adapters import HTTPAdapter
from typing import Union

from helpers import (
    COMPANY_CONCEPTS,
    COMPANY_FACTS,
    EdgarError,
    FRAMES,
    limiter,
    limiter_mapping,
    retries,
    SUBMISSIONS,
    validate_cik
)


class Edgar:
    def __init__(self, user_agent):
        self._session = Session()
        self._session.headers.update(
            {
                'User-Agent': user_agent,
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'data.sec.gov',
            }
        )
    def __enter__(self):
        self._session.mount('https://', HTTPAdapter(max_retries=retries))

        return self

    def __exit__(self, e_type, value, traceback):
        if e_type is not None:
            print(f"{e_type} : {value} : {traceback}")
        self._session.close()

        return 'ok'

    @limiter(limiter_mapping)
    def get(self, url: str):
        response = self._session.get(url)
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise EdgarError(f'{e}') from None
        return response.json()

    def get_submissions(self, cik: str):
        return self.get(f'{SUBMISSIONS}/CIK{cik}.json')

    def get_company_concepts(self, cik: str, taxonomy: str, tag: str):
        return self.get(f'{COMPANY_CONCEPTS}/CIK{cik}/{taxonomy}/{tag}.json')

    def get_company_facts(self, cik: str):
        return self.get(f'{COMPANY_FACTS}/CIK{cik}.json')

    def get_frames(
            self,
            taxonomy: str,
            tag: str,
            unit: str,
            year: str,
            quarter:  Union[int, str, None]=None,
            instantaneous: bool=True
    ):
        _quarter = (
            f'Q{quarter}' if quarter is not None and 1 <= int(quarter) <= 4 else ''
        )
        _instantaneous = 'I' if instantaneous else ''
        period = f'CY{year}{_quarter}{_instantaneous}'

        return self.get(f'{FRAMES}/{taxonomy}/{tag}/{unit}/{period}.json')
