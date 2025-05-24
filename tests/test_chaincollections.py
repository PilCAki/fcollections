"""
Unit tests for chaincollections
"""
import pytest
from chaincollections import clist, cdict, cgenerator, crange, cxrange, cset, chain

class TestChainCollections:
    def test_clist_basic(self):
        """Test basic clist functionality"""
        cl = clist([1, 2, 3, 4, 5])
        assert isinstance(cl, clist)
        assert len(cl) == 5
        assert list(cl) == [1, 2, 3, 4, 5]
    
    def test_crange(self):
        """Test crange function"""
        cr = crange(5)
        assert isinstance(cr, clist)
        assert list(cr) == [0, 1, 2, 3, 4]
    
    def test_clist_map(self):
        """Test clist map functionality"""
        cl = crange(5)
        mapped = cl.map(lambda x: x * 2)
        assert isinstance(mapped, clist)
        assert list(mapped) == [0, 2, 4, 6, 8]
    
    def test_clist_filter(self):
        """Test clist filter functionality"""
        cl = crange(10)
        filtered = cl.filter(lambda x: x % 2 == 0)
        assert isinstance(filtered, clist)
        assert list(filtered) == [0, 2, 4, 6, 8]
    
    def test_clist_conversion(self):
        """Test clist conversion methods"""
        cl = clist([1, 2, 3])
        
        # To generator
        cg = cl.to_generator()
        assert isinstance(cg, cgenerator)
        assert list(cg) == [1, 2, 3]
        
        # To set
        cs = cl.to_set()
        assert isinstance(cs, cset)
        assert cs == {1, 2, 3}
    
    def test_cgenerator_basic(self):
        """Test basic cgenerator functionality"""
        cg = cgenerator([1, 2, 3, 4, 5])
        assert isinstance(cg, cgenerator)
        assert list(cg) == [1, 2, 3, 4, 5]
    
    def test_cxrange(self):
        """Test cxrange function"""
        cxr = cxrange(5)
        assert isinstance(cxr, cgenerator)
        assert list(cxr) == [0, 1, 2, 3, 4]
    
    def test_cgenerator_map(self):
        """Test cgenerator map functionality"""
        cg = cxrange(5)
        mapped = cg.map(lambda x: x * 2)
        assert isinstance(mapped, cgenerator)
        assert list(mapped) == [0, 2, 4, 6, 8]
    
    def test_cgenerator_conversion(self):
        """Test cgenerator conversion methods"""
        cg = cgenerator([1, 2, 3])
        
        # To list
        cl = cg.to_list()
        assert isinstance(cl, clist)
        assert list(cl) == [1, 2, 3]
        
        # To set
        cs = cg.to_set()
        assert isinstance(cs, cset)
        assert cs == {1, 2, 3}
    
    def test_cdict_basic(self):
        """Test basic cdict functionality"""
        cd = cdict({'a': 1, 'b': 2, 'c': 3})
        assert isinstance(cd, cdict)
        assert cd['a'] == 1
        assert len(cd) == 3
    
    def test_cdict_methods(self):
        """Test cdict methods"""
        cd = cdict({'a': 1, 'b': 2, 'c': 3})
        
        # Keys as clist
        keys = cd.keys()
        assert isinstance(keys, clist)
        assert set(keys) == {'a', 'b', 'c'}
        
        # Values as clist
        values = cd.values()
        assert isinstance(values, clist)
        assert set(values) == {1, 2, 3}
        
        # Items as clist
        items = cd.items()
        assert isinstance(items, clist)
        assert set(items) == {('a', 1), ('b', 2), ('c', 3)}
    
    def test_cset_basic(self):
        """Test basic cset functionality"""
        cs = cset([1, 2, 3, 3, 4])
        assert isinstance(cs, cset)
        assert len(cs) == 4
        assert cs == {1, 2, 3, 4}
    
    def test_cset_operations(self):
        """Test cset operations"""
        cs1 = cset([1, 2, 3])
        cs2 = cset([2, 3, 4])
        
        # Union
        union = cs1.union(cs2)
        assert isinstance(union, cset)
        assert union == {1, 2, 3, 4}
        
        # Intersection
        intersection = cs1.intersection(cs2)
        assert isinstance(intersection, cset)
        assert intersection == {2, 3}
    
    def test_cset_conversion(self):
        """Test cset conversion methods"""
        cs = cset([1, 2, 3])
        
        # To list
        cl = cs.to_list()
        assert isinstance(cl, clist)
        assert set(cl) == {1, 2, 3}
        
        # To generator
        cg = cs.to_generator()
        assert isinstance(cg, cgenerator)
        assert set(cg) == {1, 2, 3}
    
    def test_chaining_with_new_api(self):
        """Test method chaining with new API"""
        result = (crange(10)
                 .filter(lambda x: x % 2 == 0)
                 .map(lambda x: x * 2)
                 .take(3))
        
        assert isinstance(result, clist)
        assert list(result) == [0, 4, 8]
        
    def test_chain_function(self):
        """Test the chain function with different collection types"""
        # Test with list
        result = chain([1, 2, 3])
        assert isinstance(result, clist)
        assert list(result) == [1, 2, 3]
        
        # Test with dict
        result = chain({'a': 1, 'b': 2})
        assert isinstance(result, cdict)
        assert dict(result) == {'a': 1, 'b': 2}
        
        # Test with set
        result = chain({1, 2, 3})
        assert isinstance(result, cset)
        assert set(result) == {1, 2, 3}
        
        # Test with generator
        gen = (x for x in range(3))
        result = chain(gen)
        assert isinstance(result, cgenerator)
        assert list(result) == [0, 1, 2]
        
        # Test with range
        result = chain(range(3))
        assert isinstance(result, cgenerator)
        assert list(result) == [0, 1, 2]
        
        # Test with non-collection (scalar)
        result = chain(42)
        assert isinstance(result, clist)
        assert list(result) == [42]
        
        # Test with already chain type
        cl = clist([1, 2, 3])
        result = chain(cl)
        assert result is cl  # Should return the same object, not a new one
        
    def test_chain_recursive_basic(self):
        """Test the chain function with recursive=True for basic nested structures"""
        # Test with nested dictionary
        nested_dict = {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': [4, 5, 6]}
        result = chain(nested_dict, recursive=True)
        
        # Verify result is a cdict
        assert isinstance(result, cdict)
        
        # Check that nested dict is automatically converted to cdict when accessed
        nested = result['b']
        assert isinstance(nested, cdict)
        assert nested['c'] == 2
        assert nested['d'] == 3
        
        # Check that nested list is automatically converted to clist when accessed
        nested_list = result['e']
        assert isinstance(nested_list, clist)
        assert list(nested_list) == [4, 5, 6]
        
    def test_chain_recursive_list(self):
        """Test recursive chaining with nested lists"""
        nested_list = [1, 2, [3, 4, {'a': 5}]]
        result = chain(nested_list, recursive=True)
        
        # Verify result is a clist
        assert isinstance(result, clist)
        
        # Check that nested list is automatically converted to clist when accessed
        inner_list = result[2]
        assert isinstance(inner_list, clist)
        assert list(inner_list) == [3, 4, {'a': 5}]
        
        # Check that nested dict in list is automatically converted to cdict when accessed
        nested_dict = inner_list[2]
        assert isinstance(nested_dict, cdict)
        assert nested_dict['a'] == 5
        
    def test_chain_recursive_method_chaining(self):
        """Test method chaining with recursive=True"""
        nested_data = {
            'users': [
                {'name': 'Alice', 'age': 30, 'active': True},
                {'name': 'Bob', 'age': 25, 'active': False},
                {'name': 'Charlie', 'age': 35, 'active': True}
            ]
        }
        
        result = chain(nested_data, recursive=True)
        
        # Chain methods on the nested structures
        active_users = result['users'].filter(lambda user: user['active'])
        
        assert isinstance(active_users, clist)
        assert len(active_users) == 2
        assert active_users[0]['name'] == 'Alice'
        assert active_users[1]['name'] == 'Charlie'
        
        # Further chain on the filtered results
        names = active_users.map(lambda user: user['name'])
        assert isinstance(names, clist)
        assert list(names) == ['Alice', 'Charlie']
        
    def test_chain_recursive_deep_nesting(self):
        """Test recursive chaining with deeply nested structures"""
        deep_nested = {
            'level1': {
                'level2': {
                    'level3': [
                        {'name': 'item1'},
                        {'name': 'item2'}
                    ]
                }
            }
        }
        
        result = chain(deep_nested, recursive=True)
        
        # Access deeply nested structures
        level3_list = result['level1']['level2']['level3']
        assert isinstance(level3_list, clist)
        
        # Verify we can chain on the deeply nested list
        names = level3_list.map(lambda item: item['name'])
        assert isinstance(names, clist)
        assert list(names) == ['item1', 'item2']
        
    def test_chain_recursive_preservation(self):
        """Test that recursive behavior is preserved through method calls"""
        nested_data = {
            'items': [
                {'id': 1, 'tags': ['a', 'b']},
                {'id': 2, 'tags': ['b', 'c']},
                {'id': 3, 'tags': ['a', 'c']}
            ]
        }
        
        result = chain(nested_data, recursive=True)
        
        # Filter and check if recursive behavior is preserved
        filtered = result['items'].filter(lambda item: 'a' in item['tags'])
        assert isinstance(filtered, clist)
        assert len(filtered) == 2
        
        # Verify nested structures are still chainable after filtering
        first_tags = filtered[0]['tags']
        assert isinstance(first_tags, clist)
        assert first_tags.filter(lambda tag: tag == 'a')[0] == 'a'