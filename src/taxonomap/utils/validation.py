from taxonomap.solr_request import SolrClient


client = SolrClient()


def valid_taxid(taxid: int) -> int | None:
    """
    Validates that a given taxid exists in the NCBI taxonomy database.

    Parameters
    --------
    taxid : int
        NCBI taxonomy identifier to validate.

    Returns
    -------
    int | None
        the taxid if valid, or None if not found in database.

    Raises
    ------
    ValueError
        If taxid is not an integer or is negative.

    Examples
    --------
    >>> valid_taxid(9606)
    9606

    >>> valid_taxid(999999999)
    None
    """

    if type(taxid) is not int:
        raise ValueError(f"Parameters must be a taxid, got: {taxid}")

    if taxid < 0:
        raise ValueError(f"Taxid must be a positive integer or 0, got: {taxid}")

    docs = client.query_taxo(fq=f"taxid:{taxid}", fl=None)["response"]["numFound"]

    if taxid == 0:
        return 0

    if docs == 0:
        return None

    return taxid


def convert_taxid(taxid: int | str) -> int | None:
    """
    Convert and validate a taxid (int or string).

    Parameters
    ----------
    taxid : int | str
        NCBI taxonomy identifier as integer or string.

    Returns
    -------
    int | None
        Validated taxid as integer.
    Raises
    ------
    ValueError
        If taxid format is invalid (for example non-numeric string or a negative integer).

    Examples
    --------
    >>> convert_taxid(9606)
    9606

    >>> convert_taxid("9606")
    9606

    >>> convert_taxid("invalid")
    ValueError: Invalid taxid
    """
    if type(taxid) is int:
        return valid_taxid(taxid)
    if type(taxid) is str:
        try:
            taxid_int = int(taxid)
            return valid_taxid(taxid_int)
        except ValueError:
            raise ValueError(f"taxid must be a valid integer, got: {taxid}")

    else:
        raise ValueError(f"taxid must be a positive integer or 0, got: {taxid}")


def validate_taxid_list(taxids):
    """
    DEPRECATED
    Validate a list of taxids.
    
    Parameters
    ----------
    taxids : list
        List of taxids (int or str).
    
    Returns
    -------
    list of int
        List of validated taxids.
    
    Raises
    ------
    ValueError
        If any taxid is invalid.
    
    Examples
    --------
    >>> validate_taxid_list([9606, "965", 0])
    [9606, 965, 0]
    
    >>> validate_taxid_list([9606, 999999999])
    ValueError: Invalid taxid: 999999999
    """
    validated = []
    
    for taxid in taxids:
        taxid_clean = convert_taxid(taxid)
        
        if taxid_clean is None:
            raise ValueError(f"Invalid taxid: {taxid}")
        
        validated.append(taxid_clean)
    
    return validated

def normalize_taxid(taxid):
    """
    Normalize a taxid to integer WITHOUT database validation.
    
    This function only validates FORMAT and converts to int.
    Does NOT check if the taxid exists in the database.
    
    Parameters
    ----------
    taxid : int or str
        NCBI taxonomy identifier.
    
    Returns
    -------
    int
        Normalized taxid as integer.
    
    Raises
    ------
    ValueError
        If format is invalid.
    
    Examples
    --------
    >>> normalize_taxid(9606)
    9606
    
    >>> normalize_taxid("9606")
    9606
    
    >>> normalize_taxid(-5)
    ValueError: Taxid must be >= 0
    """
    if isinstance(taxid, str):
        try:
            taxid = int(taxid)
        except ValueError:
            raise ValueError(f"Invalid taxid format: {taxid}")
    
    if not isinstance(taxid, int):
        raise ValueError(f"Taxid must be int or str, got: {type(taxid)}")
    
    if taxid < 0:
        raise ValueError(f"Taxid must be >= 0, got: {taxid}")
    
    return taxid