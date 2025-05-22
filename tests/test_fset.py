"""
Unit tests for fset functionality
"""
import pytest
from fcollections import fset, flist, frange

class TestFSet:
    def test_creation(self):
        """Test basic set creation"""
        s = fset([1, 2, 3, 4, 5])
        assert isinstance(s, fset)
        assert len(s) == 5
        assert s == {1, 2, 3, 4, 5}
        
        # Test with duplicates
        s = fset([1, 2, 2, 3, 3, 3])
        assert len(s) == 3
        assert s == {1, 2, 3}
        
    def test_conversion(self):
        """Test conversion methods"""
        s = fset([1, 2, 3, 4, 5])
        
        # To list
        lst = s.to_list()
        assert isinstance(lst, flist)
        assert sorted(lst) == [1, 2, 3, 4, 5]
        
        # To generator
        gen = s.to_generator()
        assert list(sorted(gen)) == [1, 2, 3, 4, 5]
        
        # To tuple
        tup = s.to_tuple()
        assert isinstance(tup, tuple)
        assert sorted(tup) == [1, 2, 3, 4, 5]
        
    def test_set_operations(self):
        """Test set operations"""
        s1 = fset([1, 2, 3, 4, 5])
        s2 = fset([4, 5, 6, 7, 8])
        
        # Union
        union = s1.union(s2)
        assert isinstance(union, fset)
        assert union == {1, 2, 3, 4, 5, 6, 7, 8}
        
        # Intersection
        intersection = s1.intersection(s2)
        assert isinstance(intersection, fset)
        assert intersection == {4, 5}
        
        # Difference
        difference = s1.difference(s2)
        assert isinstance(difference, fset)
        assert difference == {1, 2, 3}
        
        # Symmetric difference
        sym_diff = s1.symmetric_difference(s2)
        assert isinstance(sym_diff, fset)
        assert sym_diff == {1, 2, 3, 6, 7, 8}
        
    def test_chainable_methods(self):
        """Test chainable methods inherited from FBase"""
        s = fset(range(10))
        
        # Map
        mapped = s.map(lambda x: x * 2)
        assert isinstance(mapped, fset)
        assert mapped == {0, 2, 4, 6, 8, 10, 12, 14, 16, 18}
        
        # Filter
        filtered = s.filter(lambda x: x % 2 == 0)
        assert isinstance(filtered, fset)
        assert filtered == {0, 2, 4, 6, 8}
        
        # Take and drop
        taken = s.take(3)
        assert isinstance(taken, fset)
        assert len(taken) == 3  # Can't assert exact elements due to set ordering
        
        dropped = s.drop(7)
        assert isinstance(dropped, fset)
        assert len(dropped) <= 3  # Can't assert exact elements due to set ordering
        
    def test_new_methods(self):
        """Test new methods from FBase"""
        s = fset(range(10))
        
        # Any match
        assert s.any_match(lambda x: x > 8) is True
        assert s.any_match(lambda x: x > 10) is False
        
        # All match
        assert s.all_match(lambda x: x < 10) is True
        assert s.all_match(lambda x: x < 9) is False
        
        # Find
        assert s.find(lambda x: x > 5) in {6, 7, 8, 9}
        assert s.find(lambda x: x > 10) is None
        
    # Edge cases tests
    def test_empty_set(self):
        """Test operations on empty set"""
        s = fset([])
        assert len(s) == 0
        
        # Map on empty set
        mapped = s.map(lambda x: x * 2)
        assert len(mapped) == 0
        
        # Union with empty set
        union = s.union(fset([1, 2, 3]))
        assert union == {1, 2, 3}
        
        # Intersection with empty set
        intersection = s.intersection(fset([1, 2, 3]))
        assert intersection == set()