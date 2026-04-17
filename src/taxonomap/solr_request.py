import requests

from taxonomap.config import SOLR_BASE_ADDI, SOLR_BASE_TAXO


class SolrClient:
    """
    Client for querying the Lifemap Solr databases.

    The class provides methods to interact with two solr databases :
    - taxo : Contains taxonomy data (taxid, scientific names, ranks...)
    - addi : Contains additionnal data (lineage, descendants...) 

    Notes
    -----
    The client handles both single and batch queries, with specialised
    methods for querying multiple taxids or scientific names effficiently.

    """
    def query(self, base_url, fq, fl, rows=1):
        try:
            if isinstance(fq, str):
                fq = [fq]

            response = requests.post(
                base_url,
                data={"q": "*:*", "fq": fq, "fl": fl, "rows": rows},
                timeout=10,
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            raise Exception(f"API error: {str(e)}")

    def query_taxo(self, fq, fl, rows=1):
        """Query the taxonomy database (taxo)"""
        return self.query(SOLR_BASE_TAXO, fq, fl, rows)

    def query_addi(self, fq, fl, rows=1):
        """Query the additionnal data database (addi)"""
        return self.query(SOLR_BASE_ADDI, fq, fl, rows)
    
    def query_taxo_multiple(self, taxids, fl):
        """Query multiple taxids at once in the taxonomy databse."""
        fq = " OR ".join([f"taxid:{tid}" for tid in taxids])
        return self.query_taxo(fq=fq, fl=fl, rows=len(taxids))
    
    def query_addi_multiple(self, taxids, fl):
        """Query multiple taxids at once in the addi database. """
        fq = " OR ".join([f"taxid:{tid}" for tid in taxids])
        return self.query_addi(fq=fq, fl=fl, rows=len(taxids))
    
    def query_taxo_names_multiple(self, sci_names, fl):
        """
        Query multiple scientific names at once in the taxonomy database. 
        Uses row=len(sci_names)*10 to handle the partial matches to ensure the exact matches are included in results.

        """
        fq = " OR ".join([f'sci_name:"{name}"' for name in sci_names])
        return self.query_taxo(fq=fq, fl=fl, rows=len(sci_names) * 10)

    def result_get_ascendant(self, result):
        """Extract the lineage (the list of ancestors) from a query result."""
        docs = result["response"]["docs"][0]["ascend"]
        return docs

    def result_get_descendant(self, result):
        """Extract list of descendant taxids from a query result."""
        docs = result["response"]["docs"]
        return [d["taxid"][0] for d in docs]

    def result_get_nbdesc(self, result):
        """Extract the number of descendants from a query result."""
        docs = result["response"]["docs"][0]["nbdesc"][0]
        return docs

    def result_get_children(self, result, parent_taxid):
        """
        Extract direct children taxids from a query result.
        Filters descendants to keep only the immediate children of the specified parent taxids

        """
        docs = result["response"]["docs"]
        return [doc["taxid"][0] for doc in docs if doc["ascend"][0] == parent_taxid]

    def result_get_parent(self, result):
        """Extract the immediate parent taxid from a query result."""
        return result["response"]["docs"][0]["ascend"][0]

