import requests
from taxonomap.config import SOLR_BASE_TAXO
from taxonomap.config import SOLR_BASE_ADDI
from taxonomap.solr_request import query_taxo, query_addi
from taonomap.validation import valid_taxid,convert_taxid



def taxid_to_latin_name(taxid: int|str) -> str:
    """Convert taxid into scientific latin name"""
    taxid = convert_taxid(taxid)

    if taxid is None :
        return taxid
    if taxid == 0:
        return "LUCA"

    docs = query_taxo(fq=f"taxid:{taxid}", fl="sci_name")

    if not docs:
        raise ValueError(f"No result found for taxid: {taxid}")

    return docs[0]["sci_name"][0]
        


def latin_name_to_taxid(sci_name : str) -> int: 
    docs = query_taxo(fq=f"sci_name:{sci_name}", fl="taxid,sci_name", rows=100)
    
    #loop on query results to get the exact sci_name's taxid
    exact_matches = [doc for doc in docs if doc["sci_name"][0] == sci_name]

    if len(exact_matches) == 0:
        raise ValueError(f"Error : no exact match found for '{sci_name}'")
    
    return exact_matches[0]["taxid"][0]








#tests
if __name__ == "__main__":
    print(taxid_to_latin_name(965))
    print(latin_name_to_taxid('Oceanospirillum'))

    # mrca = get_MRCA_taxid(965,989)
    # print(f"MRCA of 965 and 989: {mrca}")