import requests

from taxonomap.config import SOLR_BASE_ADDI, SOLR_BASE_TAXO


class SolrClient:

    def query(self, base_url, fq, fl, rows=1):
        try:
            if isinstance(fq, str):
                fq = [fq]

            response = requests.post(
                base_url, data={"q": "*:*", "fq": fq, "fl": fl, "rows": rows}, timeout=10
            )
            response.raise_for_status()

            return response.json()

        except requests.RequestException as e:
            raise Exception(f"API error: {str(e)}")

    def query_taxo(self, fq, fl, rows=1):
        return self.query(SOLR_BASE_TAXO, fq, fl, rows)

    def query_addi(self, fq, fl, rows=1):
        return self.query(SOLR_BASE_ADDI, fq, fl, rows)

    def result_get_ascendant(self,result):
        docs = result["response"]["docs"][0]["ascend"]
        return docs
    
    def result_get_descendant(self, result):
        docs = result["response"]["docs"]
        return [d["taxid"][0] for d in docs]
    
    def result_get_nbdesc(self, result):
        docs = result['response']['docs'][0]['nbdesc'][0]
        return docs
    def result_get_children(self, result, parent_taxid):
        docs = result["response"]["docs"]
        return [doc["taxid"][0] for doc in docs if doc["ascend"][0] == parent_taxid]

    def result_get_parent(self, result):
        return result["response"]["docs"][0]["ascend"][0]