from taxonomap.conversions import latin_name_to_taxid, taxid_to_latin_name
from taxonomap.solr_request import query_addi
from taxonomap.utils.validation import convert_taxid




def get_all_ascendant( value: int | str ) -> list:
    """
    Get the lineage (list of ancestors) for a given taxid or name.

    Parameters
    --------
    value : int | str
        NCBI taxid (as int or string) or scientific name (string)

    Returns
    ------
    list of int
        List of ancestor taxids, orderd from the most recent parent to root.
        Returns an empty list if value is 0 (root).
        Returns None if taxid is not found in the taxonomy database

    Raises
    ------
    ValueError
        If scientific name is an empty string, or if taxid is not found.

    Examples
    -------
    >>> get_all_ascendant(965)
    [135620, 135619, 1236, 1224, 3379134, 2, 0]
    
    >>> get_all_ascendant("Oceanospirillum")
    [135620, 135619, 1236, 1224, 3379134, 2, 0]
    
    >>> get_all_ascendant(0)
    []

    """

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





def get_MRCA_taxid(*taxids) :
    """
    Finds the most recent common ancestor (MRCA) between two taxids.
    Input: 2 or more taxids
    Output: Dictionary containing the MRCA taxid number of the given taxids, and name of the MRCA taxid number.
    """
    
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
                return {
                "taxid": taxid,
                "name": taxid_to_latin_name(taxid)
            }
        
        raise ValueError("could not determine MRCA!") #supposedly it should never happen        

   




#tests
if __name__ == "__main__":
    print(get_all_ascendant("965"))
    
    print(f"MRCA of 965, 989 : {get_MRCA_taxid(965, 989)}")
    print(f"MRCA of 9606, 9685, 10090: {get_MRCA_taxid(9606, 9685, 10090)}")
