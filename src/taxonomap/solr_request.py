import requests

from taxonomap.config import SOLR_BASE_ADDI, SOLR_BASE_TAXO


def query_solr(base_url, fq, fl, rows=1):
    try:
        if isinstance(fq, str):
            fq = [fq]  # transforms argument fq in list for solr

        response = requests.post(
            base_url, data={"q": "*:*", "fq": fq, "fl": fl, "rows": rows}, timeout=10
        )

        response.raise_for_status()
        result = response.json()

        return result

    except requests.RequestException as e:
        raise Exception(f"API error: {str(e)}")


def query_taxo(fq, fl, rows=1):
    """Query taxo db"""
    return query_solr(SOLR_BASE_TAXO, fq, fl, rows)


def query_addi(fq, fl, rows=1):
    """Query addi db"""
    return query_solr(SOLR_BASE_ADDI, fq, fl, rows)
