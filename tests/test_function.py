
import pytest

from taxonomap.function import taxid_to_latin_name, get_all_ascendant,valid_taxid,convert_taxid

class Test_taxid_to_latin_name : 

    def test_invalid_type_string(self):
        """Test with string instead ofa integer"""
        with pytest.raises(ValueError):
            taxid_to_latin_name("965")


    def test_invalid_type_float(self):
        """Test with float instead of a integer"""
        with pytest.raises(ValueError):
            taxid_to_latin_name(3.14)



    def test_negative_taxid(self):
        """Test with a negative integer"""
        with pytest.raises(ValueError) :
            taxid_to_latin_name(-5)

    def test_valid_taxid(self):
        """Test with a correct taxid"""
        result = taxid_to_latin_name(965)
        assert result is not str
        assert len(result) > 0
        assert result == "Oceanospirillum"


    def test_invalid_taxid(self):
        """Test with a non-existing taxid"""
        with pytest.raises(ValueError):
            taxid_to_latin_name(999999999999999999)




class Test_get_all_ascendant : 

    def test_empty_latin_name(self):
        """Test with empty string"""
        with pytest.raises(ValueError):
            get_all_ascendant("")

    def test_negative_taxid(self):
        """Test with negative integer integer"""
        with pytest.raises(ValueError):
            get_all_ascendant(-4)

    def test_valid_latin_name(self):
        """Test with a correct latin name"""
        result = get_all_ascendant("Oceanospirillum")
        assert isinstance(result, list)
        assert result != []
        assert result == [135620, 135619, 1236, 1224, 3379134, 2, 0]


    def test_valid_taxid(self):
        """Test with a correct taxid"""
        result = get_all_ascendant(965)
        assert isinstance(result, list)
        assert result != []
        assert result == [135620, 135619, 1236, 1224, 3379134, 2, 0]




class Test_valid_taxid : 
        
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
        with pytest.raises(ValueError) :
            valid_taxid(-5)    

    def test_valid_taxid(self):
        """Test with a correct taxid"""
        result = valid_taxid(965)
        assert result == 965


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











