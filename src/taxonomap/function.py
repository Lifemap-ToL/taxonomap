import requests
from taxonomap.config import SOLR_BASE_TAXO
from taxonomap.config import SOLR_BASE_ADDI




def taxid_to_latin_name(taxid: int) -> str:
    """Convert taxid into scientific latin name"""
    
    valid_taxid(taxid)

    if taxid == 0:
        return "LUCA"

    try:
        response = requests.post(
            SOLR_BASE_TAXO,
            data={
                "q": "*:*",
                "fq": f"taxid:{taxid}",
                "fl": "sci_name"
            },
            timeout=10
        )
        response.raise_for_status() 
    except requests.RequestException as e:
        raise Exception(f"API error: {str(e)}")    
    
    result = response.json()
    docs = result["response"]["docs"]
    
    if not docs:
        raise ValueError(f"No result found for taxid: {taxid}")
    
    return docs[0]["sci_name"][0]
        





def latin_name_to_taxid(sci_name : str) -> int: 

    response = requests.post(

    SOLR_BASE_TAXO,
        data={"q": "*:*",
          "fq" : f"sci_name:{sci_name}",
            "fl": "taxid,sci_name"   
            }
    )

    result = response.json()
    docs = result["response"]["docs"]
    
    #loop on query results to get the exact sci_name's taxid
    exact_matches = [doc for doc in docs if doc["sci_name"][0] == sci_name]
    
    if len(exact_matches) == 0:
        raise ValueError(f"Error : no exact match found for '{sci_name}'")
    
    return exact_matches[0]["taxid"][0]






def get_all_ascendant( value: int | str ) -> list:

    if type(value) is str :
        if value == "":
            raise ValueError(f"Latin name cannot be empty")
        
        value = latin_name_to_taxid(value)

    valid_taxid(value)


    if value == 0:
        return []


    try:
        response = requests.post(
            SOLR_BASE_ADDI,
            data={
                "q": "*:*",
                "fq": f"taxid:{value}",
                "fl": "ascend"
            },
            timeout=10
        )
        response.raise_for_status() 

    except requests.RequestException as e:
        raise Exception(f"API error: {str(e)}")    
    
    result = response.json()
    docs = result["response"]["docs"][0]["ascend"]

    
    if not docs:
        raise ValueError(f"No result found for taxid: {value}")
    
    return docs



def valid_taxid(taxid : int) -> int :
    if type(taxid) is not int : 
        raise ValueError(f"Parameters must be a taxid")
        
    if taxid < 0:
        raise ValueError(f"Taxid must be a positive integer or 0")

    return(taxid)


def convert_taxid( taxid : int | str ) -> int:

    if type(taxid) is int:
        return taxid
    elif type(taxid) is str :
        if type(int(taxid)) is int and int(taxid) >= 0:
            return taxid
        else :
            raise ValueError(f"Taxid must be a positive integer or 0")
    
    else:
        raise ValueError(f"invalid type of parameters")








#tests
if __name__ == "__main__":
    #print(taxid_to_latin_name(965))
    #print(latin_name_to_taxid('Oceanospirillum'))
    #print(get_all_ascendant(965))
    print(convert_taxid("965"))







