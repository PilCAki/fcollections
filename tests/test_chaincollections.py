"""
Unit tests for chaincollections API (new naming convention)
"""
import pytest
from fcollections import clist, cdict, cgenerator, crange, cxrange, cset

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

class TestBackwardsCompatibility:
    def test_old_names_still_work(self):
        """Test that old fcollections names still work"""
        from fcollections import flist, fdict, fgenerator, frange, fxrange, fset
        
        # Test that old classes still work
        fl = flist([1, 2, 3])
        assert isinstance(fl, flist)
        
        fd = fdict({'a': 1})
        assert isinstance(fd, fdict)
        
        fg = fgenerator([1, 2, 3])
        assert isinstance(fg, fgenerator)
        
        fs = fset([1, 2, 3])
        assert isinstance(fs, fset)
        
        fr = frange(3)
        assert isinstance(fr, flist)
        
        fxr = fxrange(3)
        assert isinstance(fxr, fgenerator)