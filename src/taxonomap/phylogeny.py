from taxonomap.conversions import latin_name_to_taxid
from taxonomap.solr_request import query_addi
from taxonomap.utils.validation import convert_taxid




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

    docs = query_addi(fq=f"taxid:{value}", fl="ascend", rows=1)['response']["docs"][0]["ascend"]

    
    if not docs:
        raise ValueError(f"No result found for taxid: {value}")
    
    return docs





def get_MRCA_taxid(*taxids:int) -> int : #en cours
    """
    Finds the most recent common ancestor (MRCA) between two taxids.
    Input: 2 or more taxids
    Output: taxid number of MRCA of the given taxids.
    """
    #to do : return sci names
    
    if len(taxids) < 2:
        raise ValueError("Need at least 2 taxids to find MRCA")

    all_lineages = []

    for taxid in taxids:
        docs = query_addi(fq=f"taxid:{taxid}", fl="ascend")["response"]["docs"]
        
        if not docs:
            raise ValueError(f"Taxid {taxid} not found")

        lineage = docs[0]["ascend"] 
        all_lineages.append(lineage)
    
        common_ancestors = set(all_lineages[0]) #here contains ancestors of first lineage

        for lineage in all_lineages[1:]:
            common_ancestors &= set(lineage) #intersection of first set with all the others

        for taxid in all_lineages[0]: # compare first lineage with common ancestors to find the first (common ancestors possibly in mixed order)
            if taxid in common_ancestors:
                return taxid

        
        raise ValueError("could not determine MRCA!") #supposedly it should never happen        

   




#tests
if __name__ == "__main__":
    print(get_all_ascendant("965"))
    
    print(f"MRCA of 965, 989 : {get_MRCA_taxid(965, 989)}")
    print(f"MRCA of 9606, 9685, 10090: {get_MRCA_taxid(9606, 9685, 10090)}")
