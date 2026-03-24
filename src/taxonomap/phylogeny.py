from taxonomap.conversions import latin_name_to_taxid
from taxonomap.solr_request import query_addi
from taxonomap.utils.validation import convert_taxid


def get_all_ascendant(value: int | str) -> list:

    if type(value) is str:
        if value == "":
            raise ValueError("Latin name cannot be empty")

        try:
            value = convert_taxid(value)
        except ValueError:
            value = latin_name_to_taxid(value)

    value = convert_taxid(value)

    if value is None:
        return value

    if value == 0:
        return []

    docs = query_addi(fq=f"taxid:{value}", fl="ascend", rows=1)["response"]["docs"][0][
        "ascend"
    ]

    if not docs:
        raise ValueError(f"No result found for taxid: {value}")

    return docs

    # def get_MRCA_taxid(*taxids:int) -> int : #en cours
    """
    Finds the most recent common ancestor (MRCA) between two taxids.
    Input: taxid1, taxid2
    Output: taxid number of MRCA of the given taxids.
    """
    # to do : add verif for minimum 2 taxids

    # for taxid in taxids:
    #     docs = query_addi(fq=f"taxid:{taxid}", fl="ascend", rows=1)
    #     if not docs:
    #         raise ValueError(f"Taxid {taxid} not found")

    #     if len(docs1) == 0:
    #         raise ValueError(f"No result found for taxid {taxid1}")
    #     if len(docs2) == 0:
    #         raise ValueError(f"No result found for taxid {taxid2}")

    #     # get ancestors list for each
    #     lineage1 = docs1[0]["ascend"]
    #     lineage2 = docs2[0]["ascend"]

    #     #transform in set to search it easily
    #     common_ancestors = set(lineage1) & set(lineage2)
    #     print(common_ancestors)

    #     if len(common_ancestors) == 0:
    #         raise ValueError(f"There are no common ancestor found for {taxid1} and {taxid2}")

    #     #loop from the end (more specific to less)
    #     for taxid in lineage1:
    #         if taxid in common_ancestors:
    #             return taxid

    #     raise ValueError("could not determine MRCA!") #supposedly it should never happen


# tests
if __name__ == "__main__":
    print(get_all_ascendant("965"))

    # mrca = get_MRCA_taxid(965,989)
    # print(f"MRCA of 965 and 989: {mrca}")
