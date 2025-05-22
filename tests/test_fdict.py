"""
Unit tests for fdict functionality
"""
import pytest
from fcollections import fdict, flist, frange

class TestFDict:
    def test_creation(self):
        """Test basic dictionary creation"""
        d = fdict({'a': 1, 'b': 2, 'c': 3})
        assert isinstance(d, fdict)
        assert len(d) == 3
        assert d['a'] == 1
        assert d['b'] == 2
        assert d['c'] == 3
        
    def test_keys_values_items(self):
        """Test keys, values, and items methods"""
        d = fdict({'a': 1, 'b': 2, 'c': 3})
        
        keys = d.keys()
        assert isinstance(keys, flist)
        assert set(keys) == {'a', 'b', 'c'}
        
        values = d.values()
        assert isinstance(values, flist)
        assert set(values) == {1, 2, 3}
        
        items = d.items()
        assert isinstance(items, flist)
        assert set(items) == {('a', 1), ('b', 2), ('c', 3)}
        
    def test_keymap(self):
        """Test mapping function over keys"""
        d = fdict({'a': 1, 'b': 2, 'c': 3})
        result = d.keymap(lambda k: k.upper())
        assert isinstance(result, fdict)
        assert dict(result) == {'A': 1, 'B': 2, 'C': 3}
        
    def test_valmap(self):
        """Test mapping function over values"""
        d = fdict({'a': 1, 'b': 2, 'c': 3})
        result = d.valmap(lambda v: v * 10)
        assert isinstance(result, fdict)
        assert dict(result) == {'a': 10, 'b': 20, 'c': 30}
        
    def test_itemmap(self):
        """Test mapping function over items"""
        d = fdict({'a': 1, 'b': 2, 'c': 3})
        # cytoolz.itemmap returns just the keys in a generator
        # We need to use a function that returns a key-value tuple
        result = d.itemmap(lambda k_v: (k_v[0] + '_mapped', k_v[1] * 10))
        # Sort the result for consistent comparison
        assert sorted(list(result)) == ['a_mapped', 'b_mapped', 'c_mapped']
        
    def test_keyfilter(self):
        """Test filtering by key"""
        d = fdict({'a': 1, 'b': 2, 'c': 3, 'd': 4})
        result = d.keyfilter(lambda k: k in {'a', 'c'})
        assert isinstance(result, fdict)
        assert dict(result) == {'a': 1, 'c': 3}
        
    def test_valfilter(self):
        """Test filtering by value"""
        d = fdict({'a': 1, 'b': 2, 'c': 3, 'd': 4})
        result = d.valfilter(lambda v: v % 2 == 0)  # Even values
        assert isinstance(result, fdict)
        assert dict(result) == {'b': 2, 'd': 4}
        
    def test_itemfilter(self):
        """Test filtering by item"""
        d = fdict({'a': 1, 'b': 2, 'c': 3, 'd': 4})
        result = d.itemfilter(lambda k_v: k_v[0] in {'a', 'b'} and k_v[1] % 2 == 0)
        assert isinstance(result, fdict)
        assert dict(result) == {'b': 2}
        
    def test_merge(self):
        """Test merging dictionaries"""
        d1 = fdict({'a': 1, 'b': 2})
        d2 = fdict({'c': 3, 'd': 4})
        d3 = fdict({'b': 5, 'e': 6})  # Note 'b' will override
        
        # Test merging two dicts
        result = d1.merge(d2)
        assert isinstance(result, fdict)
        assert dict(result) == {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        
        # Test merging three dicts (with override)
        result = d1.merge(d2, d3)
        assert dict(result) == {'a': 1, 'b': 5, 'c': 3, 'd': 4, 'e': 6}
        
    def test_dict_operations(self):
        """Test that standard dict operations still work"""
        d = fdict({'a': 1, 'b': 2, 'c': 3})
        
        # Test getting, setting, deleting
        d['d'] = 4
        assert d['d'] == 4
        
        del d['a']
        assert 'a' not in d
        
        # Test update
        d.update({'e': 5, 'f': 6})
        assert set(d.keys()) == {'b', 'c', 'd', 'e', 'f'}
        
        # Test pop
        val = d.pop('b')
        assert val == 2
        assert 'b' not in d
    
    # Edge cases tests
    def test_empty_dict(self):
        """Test operations on empty dict"""
        d = fdict({})
        assert len(d) == 0
        assert list(d.keys()) == []
        assert list(d.values()) == []
        
        # Test mapping on empty dict
        result = d.valmap(lambda v: v * 10)
        assert len(result) == 0
        
    def test_from_collection(self):
        """Test creating fdict from collections"""
        # From list of pairs
        d = fdict([('a', 1), ('b', 2), ('c', 3)])
        assert dict(d) == {'a': 1, 'b': 2, 'c': 3}
        
        # From zip
        keys = ['x', 'y', 'z']
        values = [10, 20, 30]
        d = fdict(zip(keys, values))
        assert dict(d) == {'x': 10, 'y': 20, 'z': 30}
        
        # From keys with default value
        d = fdict.fromkeys(['a', 'b', 'c'], 0)
        assert dict(d) == {'a': 0, 'b': 0, 'c': 0}
        
    def test_to_pairs(self):
        """Test converting dict to pairs and back"""
        # To pairs
        d = fdict({'a': 1, 'b': 2, 'c': 3})
        pairs = d.to_pairs()
        assert isinstance(pairs, flist)
        assert sorted(pairs) == [('a', 1), ('b', 2), ('c', 3)]
        
        # From pairs
        pairs = [('x', 10), ('y', 20), ('z', 30)]
        d = fdict.from_pairs(pairs)
        assert isinstance(d, fdict)
        assert dict(d) == {'x': 10, 'y': 20, 'z': 30}