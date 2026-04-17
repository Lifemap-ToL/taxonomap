from taxonomap.solr_request import SolrClient
from taxonomap.utils.validation import convert_taxid, validate_taxid_list
import requests
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
    ['Homo sapiens']

    >>> taxid_to_latin_name([9606, 965, 0])
    ['Homo sapiens', 'Oceanospirillum', 'LUCA']

    Notes
    -----
    Taxid 0 returns 'LUCA' (Last Universal Common Ancestor).

    """

    if not isinstance(taxid, list):
        taxids = [taxid]  # transform into a list
    else:
        taxids = taxid

    # validation
    validated = validate_taxid_list(taxids)

    response = client.query_taxo_multiple(validated, fl="taxid,sci_name")
    docs = response["response"]["docs"]

    results = {doc["taxid"][0]: doc["sci_name"][0] for doc in docs}

    # for special case LUCA
    if 0 in validated:
        results[0] = "LUCA"

    return [results[tid] for tid in validated]


def latin_name_to_taxid(sci_name: str | list ) -> list:
    """
    Convert scientific name to NCBI taxid (the exact match). 

    Parameters
    ----------
    sci_name : str or list
        Scientific name to search for (for example : 'Homo sapiens').
        It has to be an exact match.
        The function transforms any type of input into a list.

    Returns
    -------
    list
        List of NCBI taxonomy identifiers.

    Raises
    ------
    ValueError
        If there is no exact match found for the provided input name.

    Examples
    --------
    >>> latin_name_to_taxid("Homo sapiens")
    [9606]

    >>> latin_name_to_taxid(["Homo sapiens", "Oceanospirillum", "Felis catus"])
    [9606, 965, 9685]

    """

    if not isinstance(sci_name, list):
        sci_names = [sci_name] # transform into a list
    else:
        sci_names = sci_name

    response = client.query_taxo_names_multiple(sci_names, fl='taxid,sci_name')
    docs = response["response"]["docs"]

    results = {}
    for doc in docs:
        doc_name = doc["sci_name"][0]
        doc_taxid = doc["taxid"][0]
        
        # only keep the exact match, if not found yet
        if doc_name in sci_names and doc_name not in results:
            results[doc_name] = doc_taxid
    
    result_list = []
    for name in sci_names:
        result_list.append(results[name])
    return result_list


def resolve_value(value):
    """
    Resolve a taxid or scientific name to a validated taxid.
    
    This function accepts either a taxid (as integer or string) or a
    scientific name (as string) and returns the corresponding validated taxid.
    
    Parameters
    --------
    value : int or str
        NCBI taxonomy identifier (int or numeric string), or scientific name (string).
    
    Returns
    -----
    int
        Validated NCBI taxonomy identifier
    
    Raises
    ------
    ValueError
        If value is an empty string.
    ValueError
        If the taxid is invalidd or not found in the database
    ValueError
        If the scientific name does not have an exact match in the database

    """

    if type(value) is str:
        if value == "":
            raise ValueError("Latin name cannot be empty")
        try:
            value = convert_taxid(value)
        except ValueError:
            value = latin_name_to_taxid(value)
            value = value[0]
    return convert_taxid(value)


def get_version() -> dict:
    """
    Fetch metadata from the LifeMap server.

    Returns
    -------
    dict
        A dictionary containing metadata, including the last update date
        and species counts by domain (archaea, bacteria, eukaryotes, total).

    Raises
    ------
    RuntimeError
        If the request fails or the response is not valid JSON.

    Examples
    --------
    >>> get_metadata()
    {'update': '2026-04-13', 'species': {'archaea': 13587, 'eukaryotes': 1616271, 'bacteria': 577924, 'total': 2207782}}

    """

    url = "https://lifemap-back.univ-lyon1.fr/static/metadata.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['update']
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch metadata: {e}")









# tests
if __name__ == "__main__":
    print(get_version())
# print(taxid_to_latin_name(965))
# print(latin_name_to_taxid("Oceanospirillum"))

# mrca = get_MRCA_taxid(965,989)
# print(f"MRCA of 965 and 989: {mrca}")
    # print("test élément int seul:", taxid_to_latin_name(9606))
    # print("test pour une liste:", taxid_to_latin_name([9606, 965, 0]))
    # print("test latin_name_to_taxid str seul :", latin_name_to_taxid("Homo sapiens"))
    # print("test latin_name_to_taxid en liste:", latin_name_to_taxid(["Homo sapiens", "Oceanospirillum", "Felis catus"]))