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

print(taxid_to_latin_name(965))



