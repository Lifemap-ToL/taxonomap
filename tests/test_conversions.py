import pytest

from taxonomap.conversions import taxid_to_latin_name, latin_name_to_taxid,resolve_value,get_version


class TestTaxidToLatinName:
    def test_valid_single_taxid(self):
        """Test with a single valid taxid"""
        result = taxid_to_latin_name(965)
        assert result == ["Oceanospirillum"]

    def test_valid_type_string(self):
        """Test with string instead of an integer"""
        result = taxid_to_latin_name("965")
        assert result == ["Oceanospirillum"]

    def test_valid_list_of_taxids(self):
        """Test with a list of valid taxids"""
        result = taxid_to_latin_name([9606, 965])
        assert result == ["Homo sapiens", "Oceanospirillum"]

    def test_returns_list_for_single_input(self):
        """Test that a single input returns a list, not a string"""
        result = taxid_to_latin_name(965)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_preserves_order(self):
        """Test that the order of taxids is preserved in the result"""
        result = taxid_to_latin_name([965, 9606])
        assert result == ["Oceanospirillum", "Homo sapiens"]

    def test_invalid_type_float(self):
        """Test with float instead of an integer"""
        with pytest.raises(ValueError):
            taxid_to_latin_name(3.14)

    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError):
            taxid_to_latin_name(-5)

    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        with pytest.warns(UserWarning, match="Taxids not found in database"):
            result = taxid_to_latin_name(9999999999999)
            assert result == [None]

    def test_luca_zero(self):
        """Test with taxid 0 (LUCA)"""
        result = taxid_to_latin_name(0)
        assert result == ["LUCA"]

    def test_list_with_luca(self):
        """Test with a list containing taxid 0 (LUCA)"""
        result = taxid_to_latin_name([9606, 965, 0])
        assert result == ["Homo sapiens", "Oceanospirillum", "LUCA"]

    def test_empty_string(self):
        """Test with an empty string"""
        with pytest.raises(ValueError):
            taxid_to_latin_name("") 

class TestLatinNameToTaxid:
    def test_valid_single_name(self):
        """Test with a single valid scientific name"""
        result = latin_name_to_taxid("Homo sapiens")
        assert result == [9606]

    def test_valid_list_of_names(self):
        """Test with a list of valid scientific names"""
        result = latin_name_to_taxid(["Homo sapiens", "Oceanospirillum"])
        assert result == [9606, 965]

    def test_returns_list_for_single_input(self):
        """Test that a single input returns a list, not a string"""
        result = latin_name_to_taxid("Homo sapiens")
        assert isinstance(result, list)
        assert len(result) == 1

    def test_preserves_order(self):
        """Test that the order of names is preserved in the result"""
        result = latin_name_to_taxid(["Oceanospirillum", "Homo sapiens"])
        assert result == [965, 9606]

    def test_invalid_type_float(self):
        """Test with float instead of a string"""
        with pytest.raises((ValueError, TypeError)):
            latin_name_to_taxid(3.14)

    def test_invalid_name(self):
        """Test with a non-existing scientific name"""
        with pytest.warns(UserWarning, match="No exact match found"):
            result = latin_name_to_taxid("None existing")
            assert result == [None]

    def test_partial_name_no_match(self):
        """Test that a partial name does not match (exact match required)"""
        with pytest.warns(UserWarning, match="No exact match found"):
            result = latin_name_to_taxid("Hom")
            assert result == [None]

    def test_empty_string(self):
        """Test with an empty string"""
        with pytest.raises(ValueError):
            latin_name_to_taxid("")

    def test_empty_string_in_list(self):
        """Test with an empty string in a list"""
        with pytest.raises(ValueError):
            latin_name_to_taxid(["Homo sapiens", ""])

class TestResolveValue:
    def test_valid_int_taxid(self):
        """Test with a valid integer taxid"""
        result = resolve_value(9606)
        assert result == 9606

    def test_valid_string_taxid(self):
        """Test with a valid numeric string taxid"""
        result = resolve_value("9606")
        assert result == 9606

    def test_valid_latin_name(self):
        """Test with a valid scientific name"""
        result = resolve_value("Homo sapiens")
        assert result == 9606

    def test_empty_string(self):
        """Test with an empty string"""
        with pytest.raises(ValueError, match="Latin name cannot be empty"):
            resolve_value("")

    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError):
            resolve_value(-5)

    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        result = resolve_value(9999999999999)
        assert result is None
    @pytest.mark.filterwarnings("ignore:.*No exact match found.*")
    def test_invalid_latin_name(self):
        """Test with a non-existing scientific name"""
        with pytest.raises((KeyError, ValueError)):
            resolve_value("Nonexistentus fakus")

    def test_zero_taxid(self):
        """Test with taxid 0 (LUCA)"""
        result = resolve_value(0)
        assert result == 0


class TestGetVersion:
    def test_returns_string(self):
        """Test that the version returned is a string"""
        result = get_version()
        assert isinstance(result, str)

    def test_non_empty_result(self):
        """Test that the version is not empty"""
        result = get_version()
        assert len(result) > 0

    def test_date_format(self):
        """Test that the version looks like a date (YYYY-MM-DD)"""
        result = get_version()
        parts = result.split("-")
        assert len(parts) == 3
        assert len(parts[0]) == 4  # year
        assert all(p.isdigit() for p in parts)
