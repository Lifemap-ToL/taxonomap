import pytest

from taxonomap.phylogeny import get_ascendants  # , get_MRCA_taxid


class Test_get_ascendants:
    def test_empty_latin_name(self):
        """Test with empty string"""
        with pytest.raises(ValueError):
            get_ascendants("")

    def test_negative_taxid(self):
        """Test with negative integer integer"""
        with pytest.raises(ValueError):
            get_ascendants(-4)

    def test_valid_latin_name(self):
        """Test with a correct latin name"""
        result = get_ascendants("Oceanospirillum")
        assert isinstance(result, list)
        assert result != []
        assert result == [135620, 135619, 1236, 1224, 3379134, 2, 0]

    def test_valid_taxid(self):
        """Test with a correct taxid"""
        result = get_ascendants(965)
        assert isinstance(result, list)
        assert result != []
        assert result == [135620, 135619, 1236, 1224, 3379134, 2, 0]


# class TestGetMRCA:
#     """Tests for get_MRCA_taxid function"""
#     def test_mrca_same_genus(self):
#         """test MRCA of two species from same genus"""
#         # here : Oceanospirillum (965) and Oceanospirillum linum (966)
#         mrca = get_MRCA_taxid(965, 966)
#         assert mrca == 965  # the genus itsefl
