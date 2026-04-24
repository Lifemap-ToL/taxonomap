import pytest

from taxonomap.phylogeny import     get_ascendants, get_descendants, get_tips, get_children, get_siblings, get_MRCA, get_subtree


import pytest

from taxonomap.phylogeny import (
    get_ascendants,
    get_descendants,
    get_tips,
    get_children,
    get_siblings,
    get_MRCA,
    get_subtree,
)


class TestGetAscendants:
    def test_valid_int_taxid(self):
        """Test with a valid integer taxid"""
        result = get_ascendants(965)
        assert isinstance(result, list)
        assert len(result) > 0
        assert 0 in result  # root should be in lineage

    def test_valid_string_taxid(self):
        """Test with a valid string taxid"""
        result = get_ascendants("965")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_valid_latin_name(self):
        """Test with a valid scientific name"""
        result = get_ascendants("Oceanospirillum")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_int_and_string_return_same_result(self):
        """Test that int and string taxid return the same lineage"""
        result_int = get_ascendants(965)
        result_str = get_ascendants("965")
        assert result_int == result_str

    def test_taxid_and_name_return_same_result(self):
        """Test that taxid and scientific name return the same lineage"""
        result_taxid = get_ascendants(965)
        result_name = get_ascendants("Oceanospirillum")
        assert result_taxid == result_name

    def test_lineage_ends_with_root(self):
        """Test that the lineage ends with root (0)"""
        result = get_ascendants(9606)
        assert result[-1] == 0

    def test_root_returns_empty_list(self):
        """Test that taxid 0 (root/LUCA) returns an empty list"""
        result = get_ascendants(0)
        assert result == []

    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        result = get_ascendants(9999999999999)
        assert result is None

    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError):
            get_ascendants(-5)

    def test_invalid_type_float(self):
        """Test with float instead of integer or string"""
        with pytest.raises(ValueError):
            get_ascendants(3.14)

    def test_empty_string(self):
        """Test with an empty string"""
        with pytest.raises(ValueError):
            get_ascendants("")


class TestGetDescendants:
    def test_valid_int_taxid(self):
        """Test with a valid integer taxid"""
        result = get_descendants(9682)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_valid_string_taxid(self):
        """Test with a valid string taxid"""
        result = get_descendants("9682")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_valid_latin_name(self):
        """Test with a valid scientific name"""
        result = get_descendants("Felis")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_taxid_and_name_return_same_result(self):
        """Test that taxid and scientific name return the same descendants"""
        result_taxid = get_descendants(9682)
        result_name = get_descendants("Felis")
        assert set(result_taxid) == set(result_name)

    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        result = get_descendants(9999999999999)
        assert result is None

    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError):
            get_descendants(-5)

    def test_invalid_type_float(self):
        """Test with float instead of integer or string"""
        with pytest.raises(ValueError):
            get_descendants(3.14)

    def test_empty_string(self):
        """Test with an empty string"""
        with pytest.raises(ValueError):
            get_descendants("")


class TestGetTips:
    def test_valid_int_taxid(self):
        """Test with a valid integer taxid"""
        result = get_tips(9682)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_valid_latin_name(self):
        """Test with a valid scientific name"""
        result = get_tips("Felis")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_tips_are_subset_of_descendants(self):
        """Test that tips are a subset of descendants"""
        tips = get_tips(9682)
        descendants = get_descendants(9682)
        assert set(tips).issubset(set(descendants))

    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        result = get_tips(9999999999999)
        assert result is None

    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError):
            get_tips(-5)

    def test_invalid_type_float(self):
        """Test with float instead of integer or string"""
        with pytest.raises(ValueError):
            get_tips(3.14)


class TestGetChildren:
    def test_valid_int_taxid(self):
        """Test with a valid integer taxid"""
        result = get_children(9682)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_valid_latin_name(self):
        """Test with a valid scientific name"""
        result = get_children("Felis")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_taxid_and_name_return_same_result(self):
        """Test that taxid and name return the same children"""
        result_taxid = get_children(9682)
        result_name = get_children("Felis")
        assert set(result_taxid) == set(result_name)

    def test_children_are_subset_of_descendants(self):
        """Test that direct children are a subset of all descendants"""
        children = get_children(9682)
        descendants = get_descendants(9682)
        assert set(children).issubset(set(descendants))

    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        result = get_children(9999999999999)
        assert result is None

    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError):
            get_children(-5)

    def test_invalid_type_float(self):
        """Test with float instead of integer or string"""
        with pytest.raises(ValueError):
            get_children(3.14)


class TestGetSiblings:
    def test_valid_int_taxid(self):
        """Test with a valid integer taxid"""
        result = get_siblings(9685)
        assert isinstance(result, list)

    def test_valid_latin_name(self):
        """Test with a valid scientific name"""
        result = get_siblings("Felis catus")
        assert isinstance(result, list)

    def test_siblings_do_not_contain_self(self):
        """Test that the taxid itself is not in its siblings"""
        result = get_siblings(9685)
        assert 9685 not in result

    def test_taxid_and_name_return_same_result(self):
        """Test that taxid and name return the same siblings"""
        result_taxid = get_siblings(9685)
        result_name = get_siblings("Felis catus")
        assert set(result_taxid) == set(result_name)

    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        result = get_siblings(9999999999999)
        assert result is None

    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError):
            get_siblings(-5)

    def test_invalid_type_float(self):
        """Test with float instead of integer or string"""
        with pytest.raises(ValueError):
            get_siblings(3.14)


class TestGetMRCA:
    def test_valid_int_taxids(self):
        """Test with a list of valid integer taxids"""
        result = get_MRCA([9606, 9685])
        assert isinstance(result, dict)
        assert "taxid" in result
        assert "name" in result

    def test_valid_string_taxids(self):
        """Test with a list of valid string taxids"""
        result = get_MRCA(["9606", "9685"])
        assert isinstance(result, dict)
        assert "taxid" in result
        assert "name" in result

    def test_int_and_string_return_same_result(self):
        """Test that int and string taxids return the same MRCA"""
        result_int = get_MRCA([9606, 9685])
        result_str = get_MRCA(["9606", "9685"])
        assert result_int == result_str

    def test_more_than_two_taxids(self):
        """Test with more than two taxids"""
        result = get_MRCA([9606, 9685, 9615])
        assert isinstance(result, dict)
        assert "taxid" in result
        assert "name" in result

    def test_only_one_taxid(self):
        """Test with only one taxid raises ValueError"""
        with pytest.raises(ValueError, match="at least 2"):
            get_MRCA([9606])

    def test_empty_list(self):
        """Test with an empty list raises ValueError"""
        with pytest.raises(ValueError, match="at least 2"):
            get_MRCA([])

    def test_invalid_taxid_in_list(self):
        """Test with a non-existing taxid in the list"""
        with pytest.raises(ValueError):
            get_MRCA([9606, 9999999999999])

    def test_negative_taxid_in_list(self):
        """Test with a negative taxid in the list"""
        with pytest.raises(ValueError):
            get_MRCA([9606, -5])

    def test_float_taxid_in_list(self):
        """Test with a float taxid in the list"""
        with pytest.raises(ValueError):
            get_MRCA([9606, 3.14])

    def test_same_taxid_twice(self):
        """Test with the same taxid twice returns that taxid's lineage"""
        result = get_MRCA([9606, 9606])
        assert isinstance(result, dict)
        assert result["taxid"] == 9606


class TestGetSubtree:
    def test_valid_int_taxids(self):
        """Test with a list of valid integer taxids"""
        result = get_subtree([9606, 9685])
        assert isinstance(result, str)
        assert result.endswith(";")

    def test_valid_string_taxids(self):
        """Test with a list of valid string taxids"""
        result = get_subtree(["9606", "9685"])
        assert isinstance(result, str)
        assert result.endswith(";")

    def test_newick_format(self):
        """Test that the result is a valid Newick string"""
        result = get_subtree([9606, 9685])
        assert result.startswith("(")
        assert ");" in result or result.endswith(";")

    def test_leaves_in_result(self):
        """Test that all input taxids appear in the Newick string"""
        result = get_subtree([9606, 9685])
        assert "9606" in result
        assert "9685" in result

    def test_more_than_two_taxids(self):
        """Test with more than two taxids"""
        result = get_subtree([9606, 9685, 9615])
        assert isinstance(result, str)
        assert "9606" in result
        assert "9685" in result
        assert "9615" in result

    def test_only_one_taxid(self):
        """Test with only one taxid raises ValueError"""
        with pytest.raises(ValueError, match="at least 2"):
            get_subtree([9606])

    def test_empty_list(self):
        """Test with an empty list raises ValueError"""
        with pytest.raises(ValueError, match="at least 2"):
            get_subtree([])

    def test_invalid_taxid_in_list(self):
        """Test with a non-existing taxid in the list"""
        with pytest.raises(ValueError):
            get_subtree([9606, 9999999999999])

    def test_negative_taxid_in_list(self):
        """Test with a negative taxid in the list"""
        with pytest.raises(ValueError):
            get_subtree([9606, -5])

    def test_float_taxid_in_list(self):
        """Test with a float taxid in the list"""
        with pytest.raises(ValueError):
            get_subtree([9606, 3.14])