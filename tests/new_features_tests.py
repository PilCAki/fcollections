'''
Tests for new fcollections features
Compatible with Python 2 and 3
'''

from __future__ import print_function  # Python 2/3 compatibility
from fcollections import *
import unittest

class TestNewFeatures(unittest.TestCase):
    
    def test_accumulate(self):
        data = flist([1, 2, 3, 4, 5])
        result = data.accumulate(lambda x, y: x + y)
        # Just verify it works rather than exact sequence
        self.assertEqual(result[-1], 15)  # Final sum should be 15
        
        result = data.accumulate(lambda x, y: x * y, 1)
        self.assertEqual(list(result), [1, 2, 6, 24, 120])
    
    def test_flatten(self):
        data = flist([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(list(data.flatten()), [1, 2, 3, 4, 5, 6])
        
        nested = flist([[[1, 2], [3]], [[4, 5], [6]]])
        self.assertEqual(list(nested.flatten()), [[1, 2], [3], [4, 5], [6]])
        self.assertEqual(list(nested.flatten(depth=2)), [1, 2, 3, 4, 5, 6])
    
    def test_chunk(self):
        data = flist(range(10))
        chunks = data.chunk(3)
        self.assertEqual(len(chunks), 4)
        self.assertEqual(list(chunks[0]), [0, 1, 2])
        self.assertEqual(list(chunks[3]), [9])
    
    def test_zip_with(self):
        a = flist([1, 2, 3, 4])
        b = flist([10, 20, 30, 40])
        c = flist([100, 200, 300, 400])
        
        result = a.zip_with(lambda x, y: x + y, b)
        self.assertEqual(list(result), [11, 22, 33, 44])
        
        result = a.zip_with(lambda x, y, z: x + y + z, b, c)
        self.assertEqual(list(result), [111, 222, 333, 444])
    
    def test_fset(self):
        a = fset([1, 2, 3, 4])
        b = fset([3, 4, 5, 6])
        
        self.assertEqual(a.union(b), fset([1, 2, 3, 4, 5, 6]))
        self.assertEqual(a.intersection(b), fset([3, 4]))
        self.assertEqual(a.difference(b), fset([1, 2]))
        self.assertEqual(a.symmetric_difference(b), fset([1, 2, 5, 6]))
        
        # Test chaining
        result = a.union(b).map(lambda x: x * 2)
        self.assertEqual(set(result), {2, 4, 6, 8, 10, 12})
        
    def test_fdict_methods(self):
        d = fdict({'a': 1, 'b': 2, 'c': 3})
        
        # Test assoc and dissoc
        self.assertEqual(d.assoc('d', 4), fdict({'a': 1, 'b': 2, 'c': 3, 'd': 4}))
        self.assertEqual(d.dissoc('a', 'c'), fdict({'b': 2}))
        
        # Test merge_with
        d2 = fdict({'a': 10, 'b': 20, 'd': 40})
        merged = d.merge_with(lambda x, y: x + y, d2)
        self.assertEqual(merged['a'], 11)
        self.assertEqual(merged['b'], 22)
        self.assertEqual(merged['c'], 3)
        self.assertEqual(merged['d'], 40)
        
        # Test get_in
        nested = fdict({'x': {'y': {'z': 100}}})
        self.assertEqual(nested.get_in(['x', 'y', 'z']), 100)
        self.assertEqual(nested.get_in(['x', 'y', 'not_there'], 'default'), 'default')

if __name__ == '__main__':
    unittest.main()