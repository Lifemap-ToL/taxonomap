

def valid_taxid(taxid : int) -> int :
    if type(taxid) is not int : 
        raise ValueError(f"Parameters must be a taxid, got: {taxid}")
        
    if taxid < 0:
        raise ValueError(f"Taxid must be a positive integer or 0, got: {taxid}")
    
    docs = query_taxo(fq=f"taxid:{taxid}", fl="taxid", rows=1)
    
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

