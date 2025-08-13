# Edgar
A requests package for EDGAR, a data product of the Securities and Exchange Commission (SEC).

Specify your `user_agent` and query selection parameters in `app.py`. In the demonstration case, `Edgar.get_submissions()` is used. This particular function requires a `cik` or Central Index Key. This is the primary key of SEC filer-entities. The activities of `get_submission`, `get_company_concepts`, `get_company_facts` and `get_frames` are variously described by SEC.

https://www.sec.gov/search-filings/edgar-application-programming-interfaces
