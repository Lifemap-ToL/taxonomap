import requests

def taxid_to_latin_name(taxid : int): 

    response = requests.post(

    "https://lifemap-back.univ-lyon1.fr/solr/taxo/select",
        data={"q": "*:*",
          "fq" : f"taxid:{taxid}",
          "fl" : "sci_name"}
    )

    result = response.json()
    return(result["response"]["docs"][0]["sci_name"][0])


def latin_name_to_taxid(sci_name : str): 

    response = requests.post(

    "https://lifemap-back.univ-lyon1.fr/solr/taxo/select",
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


#tests
if __name__ == "__main__":
    print(taxid_to_latin_name(965))
    print(latin_name_to_taxid('Oceanospirillum'))



