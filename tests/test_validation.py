import pytest

from taxonomap.utils.validation import convert_taxid, valid_taxid


class Test_valid_taxid:
    def test_invalid_type_list(self):
        """Test with a correct latin name"""
        with pytest.raises(ValueError):
            valid_taxid([])

    def test_invalid_type_string(self):
        """Test with string instead of a integer"""
        with pytest.raises(ValueError):
            valid_taxid("965")

    def test_invalid_type_float(self):
        """Test with float instead of a integer"""
        with pytest.raises(ValueError):
            valid_taxid(3.14)

    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError):
            valid_taxid(-5)

    def test_valid_taxid(self):
        """Test with a correct taxid"""
        result = valid_taxid(965)
        assert result == 965

    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        result = valid_taxid(9999999999999)
        assert result is None


class TestConvertTaxid:
    def test_valid_int_taxid(self):
        """Test with a valid integer taxid"""
        result = convert_taxid(9606)
        assert result == 9606

    def test_valid_string_taxid(self):
        """Test with a valid string representation of taxid"""
        result = convert_taxid("9606")
        assert result == 9606

    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError):
            convert_taxid(-5)

    def test_invalid_string_float(self):
        """Test with a float as string"""
        with pytest.raises(ValueError):
            convert_taxid("9.65")

    def test_invalid_type_float(self):
        """Test with a float"""
        with pytest.raises(ValueError):
            convert_taxid(3.14)

    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        result = convert_taxid(9999999999999)
        assert result is None
