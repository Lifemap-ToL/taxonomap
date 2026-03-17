
import pytest

from taxonomap.function import taxid_to_latin_name




def test_invalid_type_string():
    """Test with string instead ofa integer"""
    with pytest.raises(ValueError):
        taxid_to_latin_name("965")



def test_invalid_type_float():
    """Test with float instead of a integer"""
    with pytest.raises(ValueError):
        taxid_to_latin_name(3.14)



def test_negative_taxid():
    """Test with a negative integer"""
    with pytest.raises(ValueError) :
        taxid_to_latin_name(-5)



def test_zero_taxid():
    """Test with taxid = 0"""
    with pytest.raises(ValueError):

        taxid_to_latin_name(0)





def test_valid_taxid():
    """Test with a correct taxid"""
    result = taxid_to_latin_name(965)
    assert result is not str
    assert len(result) > 0




def test_invalid_taxid():
    """Test with a non-existing taxid"""
    with pytest.raises(ValueError):
        taxid_to_latin_name(999999999999999999)












