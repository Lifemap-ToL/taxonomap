from taxonomap.conversions import taxid_to_latin_name, resolve_value
from taxonomap.utils.validation import validate_taxid_list
from taxonomap.solr_request import SolrClient


def get_ascendant(value: int | str) -> list:
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
    client = SolrClient()

    value = resolve_value(value)

    if value is None:
        return value

    if value == 0:
        return []

    docs = client.result_get_ascendant(
        client.query_addi(fq=f"taxid:{value}", fl="ascend", rows=1)
    )

    if not docs:
        raise ValueError(f"No result found for taxid: {value}")

    return docs


def get_descendants(value: int | str) -> list:
    """
    Get all descendant taxids for a given taxid or name.

    Parameters
    ----------
    value : int | str
        NCBI taxid (as int or string) or scientific name (string)

    Returns
    -------
    list of int
        List of descendant taxids.

    Examples
    -------
    >>> get_all_descendants(9682)
    [9683, 9685, 9688, ...]

    >>> get_all_descendants("Felis")
    [9683, 9685, 9688, ...]
    """
    client = SolrClient()

    value = resolve_value(value)

    if value is None:
        return value

    docs = client.result_get_descendant(
        client.query_addi(fq=f"ascend:{value}", fl="taxid", rows=1000000)
    )

    return docs


def get_tips(value: int | str) -> list:
    """
    Get all terminal (leaf) taxids for a given taxid or name.

    A tip is a taxon with no descendants (nbdesc == 1).

    Parameters
    ----------
    value : int | str
        NCBI taxid (as int or string) or scientific name (string)

    Returns
    -------
    list of int
        List of terminal (leaf) taxids.

    Examples
    -------
    >>> get_tips(9682)
    [9683, 9685, 9688, ...]

    >>> get_tips("Felis")
    [9683, 9685, 9688, ...]
    """
    client = SolrClient()

    value = resolve_value(value)

    if value is None:
        return value

    descendants = client.result_get_descendant(
        client.query_addi(fq=f"ascend:{value}", fl="taxid", rows=1000000)
    )

    tips = []
    for taxid in descendants:
        result = client.query_taxo(fq=f"taxid:{taxid}", fl="nbdesc")
        nbdesc = client.result_get_nbdesc(result)
        if nbdesc == 1:
            tips.append(taxid)

    return tips


def get_children(value: int | str) -> list:
    """
    Get the direct children taxids for a given taxid or name.

    Parameters
    ----------
    value : int | str
        NCBI taxid (as int or string) or scientific name (string)

    Returns
    -------
    list of int
        List of direct children taxids.

    Examples
    -------
    >>> get_children(9682)
    [9683, 9685]

    >>> get_children("Felis")
    [9683, 9685]
    """
    client = SolrClient()

    value = resolve_value(value)

    if value is None:
        return value

    result = client.query_addi(fq=f"ascend:{value}", fl="taxid,ascend", rows=1000000)
    return client.result_get_children(result, value)


def get_siblings(value: int | str) -> list:
    """
    Get the sibling taxids for a given taxid or name.

    Siblings are the other children of the parent taxon,
    excluding the given taxon itself.

    Parameters
    ----------
    value : int | str
        NCBI taxid (as int or string) or scientific name (string)

    Returns
    -------
    list of int
        List of sibling taxids.

    Examples
    -------
    >>> get_siblings(9685)
    [9683, 9688, ...]

    >>> get_siblings("Felis catus")
    [9683, 9688, ...]
    """
    client = SolrClient()

    value = resolve_value(value)

    if value is None:
        return value

    result = client.query_addi(fq=f"taxid:{value}", fl="ascend", rows=1)
    parent = client.result_get_parent(result)

    siblings = get_children(parent)
    siblings = [s for s in siblings if s != value]

    return siblings


def get_MRCA(taxids:list) -> dict:
    """
    Find the Most Recent Common Ancestor (MRCA) of multiple taxids.

    Parameters
    --------
    taxids : list of int | list of str
        List containing two or more NCBI taxonomy identifiers.

    Returns
    -------
    dict
        Dictionary containing:

        - taxid : int
            NCBI taxonomy ID of the MRCA
        - name : str
            Scientific name of the MRCA

    Raises
    -----
    ValueError
        If fewer than 2 taxids are provided.
    ValueError
        If a taxid is not found in the database.
    ValueError
        If no common ancestor exists between the provided taxids. (supposedly, never happens)

    Examples
    --------
    Find MRCA of human and cat:

    >>> get_MRCA([9606, 9685])
    {'taxid': 1437010, 'name': 'Boreoeutheria'}

    or 

    >>> get_MRCA(['9606', '9685'])
    {'taxid': 1437010, 'name': 'Boreoeutheria'}


    Notes
    -----
    The algorithm uses set intersection to find common ancestors,
    then returns the most recent one by comparing the intersected
    set to the first lineage - which is ordered from most recent
    to oldest ancestor.

    """
    client = SolrClient()

    if not isinstance(taxids, list):
        taxids_list = [taxids]
    else:
        taxids_list = taxids

    if len(taxids_list) < 2:
        raise ValueError("Need at least 2 taxids to find MRCA")

    validated = validate_taxid_list(taxids_list)

    response = client.query_addi_multiple(validated, fl="taxid,ascend")
    docs = response["response"]["docs"]    

    lineage_dict = {doc["taxid"][0]: doc["ascend"] for doc in docs}
    all_lineages = [lineage_dict[tid] for tid in validated]

    lineages_sets = [set(lineage) for lineage in all_lineages]
    common_ancestors = set.intersection(*lineages_sets)

    if not common_ancestors:
        raise ValueError("No common ancestor found!")

    for taxid in all_lineages[0]:
        if taxid in common_ancestors:
            return {"taxid": taxid, "name": taxid_to_latin_name(taxid)[0]}

    raise ValueError("could not determine MRCA!")  # supposedly it should never happen
