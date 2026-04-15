import pytest

from taxonomap.conversions import taxid_to_latin_name


class Test_taxid_to_latin_name:
    def test_valid_type_string(self):
        """Test with string instead ofa integer"""
        result = taxid_to_latin_name("965")
        assert result == ["Oceanospirillum"]

    def test_invalid_type_float(self):
        """Test with float instead of a integer"""
        with pytest.raises(ValueError):
            taxid_to_latin_name(3.14)

    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError):
            taxid_to_latin_name(-5)

    def test_valid_taxid(self):
        """Test with a correct taxid"""
        result = taxid_to_latin_name(965)
        assert result is not str
        assert len(result) > 0
        assert result == ["Oceanospirillum"]

    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        with pytest.raises(ValueError, match="Invalid taxid"):
            taxid_to_latin_name(9999999999999)

    def test_list_multiple_taxids(self):
        """Test with a list of taxids"""
        result = taxid_to_latin_name([9606, 965, 0])
        assert result == ["Homo sapiens", "Oceanospirillum", "LUCA"]
    
    def test_luca_zero(self):
        """Test with taxid 0 (LUCA)"""
        result = taxid_to_latin_name(0)
        assert result == ["LUCA"]
