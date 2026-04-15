from taxonomap.solr_request import SolrClient
from taxonomap.utils.validation import convert_taxid

client = SolrClient()


def taxid_to_latin_name(taxid: int | str | list) -> list:
    """
    Convert NCBI taxid to scientific name

    Parameters
    ----------
    taxid : int | str | list
        NCBI taxonomy identifier(s). It can be provided as integer, a string, or a list.
        The function transforms any type of input into a list.

    Returns
    -------
    list
        Returns a list of scientific names (for example : 'Homo sapiens'), even for a single input

    Raises
    ------
    ValueError
        If taxid is invalid or not found in database.

    Examples
    --------
    >>> taxid_to_latin_name(9606)
    'Homo sapiens'

    >>> taxid_to_latin_name("965")
    'Oceanospirillum'

    Notes
    -----
    Taxid 0 returns 'LUCA' (Last Universal Common Ancestor).

    """

    if isinstance(taxid, list):
        results = []
        for t in taxid:
            latin_name = taxid_to_latin_name()
            results.append(latin_name)
        return results

    taxid = convert_taxid(taxid)

    if taxid is None:
        return taxid
    if taxid == 0:
        return "LUCA"

    docs = client.query_taxo(fq=f"taxid:{taxid}", fl="sci_name")["response"]["docs"]

    if not docs:
        raise ValueError(f"No result found for taxid: {taxid}")

    return docs[0]["sci_name"][0]


def latin_name_to_taxid(sci_name: str) -> int:
    """
    Convert scientific name to NCBI taxid (the exact match).

    Parameters
    ----------
    sci_name : str
        Scientific name to search for (for example : 'Homo sapiens').
        It has to be an exact match.

    Returns
    -------
    int
        NCBI taxonomy identifier.

    Raises
    ------
    ValueError
        If there is no exact match found for the provided input name.


    Examples
    --------
    >>> latin_name_to_taxid("Homo sapiens")
    9606

    >>> latin_name_to_taxid("Oceanospirillum")
    965

    """

    docs = client.query_taxo(fq=f"sci_name:{sci_name}", fl="taxid,sci_name", rows=100)[
        "response"
    ]["docs"]

    # loop on query results to get the exact sci_name's taxid
    exact_matches = [doc for doc in docs if doc["sci_name"][0] == sci_name]

    if len(exact_matches) == 0:
        raise ValueError(f"Error : no exact match found for '{sci_name}'")

    return exact_matches[0]["taxid"][0]


def resolve_value(value):
    if type(value) is str:
        if value == "":
            raise ValueError("Latin name cannot be empty")
        try:
            value = convert_taxid(value)
        except ValueError:
            value = latin_name_to_taxid(value)
    return convert_taxid(value)


# tests
if __name__ == "__main__":
# print(taxid_to_latin_name(965))
# print(latin_name_to_taxid("Oceanospirillum"))

# mrca = get_MRCA_taxid(965,989)
# print(f"MRCA of 965 and 989: {mrca}")
    print("test élément int seul:", taxid_to_latin_name(9606))
    print("test pour une liste:", taxid_to_latin_name([9606, 965, 0]))