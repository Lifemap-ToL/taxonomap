import requests
from config import SOLR_BASE_TAXO
from config import SOLR_BASE_ADDI




def taxid_to_latin_name(taxid: int|str) -> str:
    """Convert taxid into scientific latin name"""
    
    taxid = convert_taxid(taxid)

    if taxid is None :
        return taxid

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

    if type(value) is str:
        if value == "":
            raise ValueError(f"Latin name cannot be empty")
        
        try:
            value = convert_taxid(value)
        except ValueError:
            value = latin_name_to_taxid(value)

    value = convert_taxid(value)

    if value is None:
        return value

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
        raise ValueError(f"Parameters must be a taxid, got: {taxid}")
        
    if taxid < 0:
        raise ValueError(f"Taxid must be a positive integer or 0, got: {taxid}")
    
    try:
        response = requests.post(
            SOLR_BASE_TAXO,
            data={
                "q": "*:*",
                "fq": f"taxid:{taxid}",
            },
            timeout=10
        )
        response.raise_for_status() 

    except requests.RequestException as e:
        raise Exception(f"API error: {str(e)}")  

    result = response.json()
    docs = result["response"]["numFound"]
    if docs == 0:
        return None

    return taxid



def convert_taxid( taxid : int | str ) -> int:
    if type(taxid) is int:
        return valid_taxid(taxid)
    if type(taxid) is str :
        try:
            taxid_int = int(taxid)
            return valid_taxid(taxid_int)
        except ValueError:
            raise ValueError(f"taxid must be a valid integer, got: {taxid}")
    
    else:
        raise ValueError(f"taxid must be a positive integer or 0, got: {taxid}")


def get_MRCA_taxid(taxid1:int, taxid2:int):
    

    try:
        response1 = requests.post(
            SOLR_BASE_ADDI,
            data={
                "q": "*:*",
                "fq": f"taxid:{taxid1}",
                "fl": "ascend"
            }
        )        
        response1.raise_for_status() 

        response2 = requests.post(
            SOLR_BASE_ADDI,
            data={
                "q": "*:*",
                "fq": f"taxid:{taxid2}",
                "fl": "ascend"
            }
        )
        response2.raise_for_status()

        result1 = response1.json()
        docs1 = result1["response"]["docs"]

        result2 = response2.json()
        docs2 = result2["response"]["docs"]
        
        if len(docs1) == 0:
            raise ValueError(f"No result found for taxid {taxid1}")
        if len(docs2) == 0:
            raise ValueError(f"No result found for taxid {taxid2}")
        
        # get ancestors list for each  
        lineage1 = docs1[0]["ascend"]
        lineage2 = docs2[0]["ascend"]

        #transform in set to search it easily
        common_ancestors = set(lineage1) & set(lineage2)
        print(common_ancestors)

        if len(common_ancestors) == 0:
            raise ValueError(f"There are no common ancestor found for {taxid1} and {taxid2}")

        #loop from the end (more specific to less)
        for taxid in lineage1:
            if taxid in common_ancestors:
                return taxid

        
        raise ValueError("could not determine MRCA!") #supposedly it should never happen        

   
    
    except requests.RequestException as e:
            raise Exception(f"API error: {str(e)}")




#tests
if __name__ == "__main__":
    print(taxid_to_latin_name(965))
    print(latin_name_to_taxid('Oceanospirillum'))
    print(get_all_ascendant(965))
    print(convert_taxid("965"))
    mrca = get_MRCA_taxid(965,989)
    print(f"MRCA of 965 and 989: {mrca}")







