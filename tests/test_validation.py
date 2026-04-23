import pytest

from taxonomap.utils.validation import convert_taxid, valid_taxid, validate_taxid_list


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



class TestValidateTaxidList:
    def test_valid_int_list(self):
        """Test with a list of valid integer taxids"""
        result = validate_taxid_list([9606, 965])
        assert result == [9606, 965]

    def test_valid_string_list(self):
        """Test with a list of valid string taxids"""
        result = validate_taxid_list(["9606", "965"])
        assert result == [9606, 965]

    def test_valid_mixed_list(self):
        """Test with a mixed list of int and string taxids"""
        result = validate_taxid_list([9606, "965"])
        assert result == [9606, 965]

    def test_empty_list(self):
        """Test with an empty list"""
        result = validate_taxid_list([])
        assert result == []

    def test_single_valid_taxid(self):
        """Test with a list containing a single valid taxid"""
        result = validate_taxid_list([9606])
        assert result == [9606]

    def test_invalid_taxid_in_list(self):
        """Test with a list containing a non-existing taxid"""
        with pytest.raises(ValueError, match="Invalid taxid"):
            validate_taxid_list([9606, 9999999999999])

    def test_negative_taxid_in_list(self):
        """Test with a list containing a negative taxid"""
        with pytest.raises(ValueError):
            validate_taxid_list([9606, -5])

    def test_float_taxid_in_list(self):
        """Test with a list containing a float"""
        with pytest.raises(ValueError):
            validate_taxid_list([9606, 3.14])

    def test_string_float_in_list(self):
        """Test with a list containing a float as string"""
        with pytest.raises(ValueError):
            validate_taxid_list([9606, "9.65"])

    def test_all_invalid_taxids(self):
        """Test with a list of only invalid taxids"""
        with pytest.raises(ValueError):
            validate_taxid_list([9999999999999, 8888888888888])

    def test_invalid_taxid_error_message(self):
        """Test that the error message contains the invalid taxid"""
        with pytest.raises(ValueError, match="9999999999999"):
            validate_taxid_list([9999999999999])

    def test_preserves_order(self):
        """Test that the order of taxids is preserved"""
        result = validate_taxid_list([965, 9606, 10090])
        assert result == [965, 9606, 10090]


