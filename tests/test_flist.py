"""
Unit tests for flist functionality
"""
import pytest
import numpy as np
from fcollections import flist, frange

class TestFList:
    def test_creation(self):
        """Test basic list creation"""
        a = flist([1, 2, 3, 4, 5])
        assert isinstance(a, flist)
        assert len(a) == 5
        assert list(a) == [1, 2, 3, 4, 5]
        
    def test_map(self):
        """Test mapping function over a list"""
        a = frange(5)
        result = a.map(lambda x: x * 2)
        assert isinstance(result, flist)
        assert list(result) == [0, 2, 4, 6, 8]
        
    def test_reduce(self):
        """Test reduce functionality"""
        a = frange(5)
        result = a.reduce(lambda a, b: a + b)
        assert result == 10
        
        # Test with initializer
        result = a.reduce(lambda a, b: a + b, 5)
        assert result == 15
        
    def test_filter(self):
        """Test filtering elements"""
        a = frange(10)
        result = a.filter(lambda x: x % 2 == 0)  # Even numbers
        assert isinstance(result, flist)
        assert list(result) == [0, 2, 4, 6, 8]
        
    def test_concat(self):
        """Test concatenation of nested lists"""
        a = flist([frange(3), frange(3, 6), frange(6, 9)])
        result = a.concat()
        assert isinstance(result, flist)
        assert list(result) == [0, 1, 2, 3, 4, 5, 6, 7, 8]
        
    def test_take_drop(self):
        """Test take and drop methods"""
        a = frange(10)
        take_result = a.take(3)
        assert list(take_result) == [0, 1, 2]
        
        drop_result = a.drop(7)
        assert list(drop_result) == [7, 8, 9]
        
    def test_first_second_last(self):
        """Test first, second, last accessors"""
        a = frange(10)
        assert a.first() == 0
        assert a.second() == 1
        assert a.last() == 9
        
    def test_interleave_interpose(self):
        """Test interleaving and interposing"""
        a = frange(3)
        b = frange(10, 13)
        interleaved = a.interleave(b)
        assert list(interleaved) == [0, 10, 1, 11, 2, 12]
        
        interposed = a.interpose("X")
        assert list(interposed) == [0, "X", 1, "X", 2]
        
    def test_partition(self):
        """Test partitioning elements"""
        a = frange(10)
        result = a.partition(3)
        assert len(result) == 3
        assert [list(p) for p in result] == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        
        # Test partition_all (includes incomplete chunks)
        result = a.partition_all(4)
        assert len(result) == 3
        assert [list(p) for p in result] == [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
        
    def test_groupby(self):
        """Test grouping elements by key"""
        a = frange(10)
        is_even = lambda i: 'even' if i % 2 == 0 else 'odd'
        result = a.groupby(is_even)
        assert 'even' in result
        assert 'odd' in result
        assert list(result['even']) == [0, 2, 4, 6, 8]
        assert list(result['odd']) == [1, 3, 5, 7, 9]
        
    def test_sliding_window(self):
        """Test sliding window functionality"""
        a = frange(5)
        result = a.sliding_window(3).to_list()
        assert len(result) == 3
        assert [list(w) for w in result] == [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
        
    def test_pipe(self):
        """Test pipe functionality"""
        a = frange(10)
        result = a.pipe(lambda x: x * 3, np.asarray, np.std)
        # The actual calculated value is close to 2.87
        assert result == pytest.approx(2.87, abs=0.01)
        
    def test_pipe_map(self):
        """Test pipe_map functionality"""
        a = frange(5)
        result = a.pipe_map(lambda x: x - 4, lambda x: x + 4, lambda x: x * 2)
        assert list(result) == [0, 2, 4, 6, 8]
        
    def test_sort(self):
        """Test sorting methods"""
        a = flist([3, 1, 4, 2, 5])
        sorted_list = a.sort()
        assert list(sorted_list) == [1, 2, 3, 4, 5]
        
        # Test sort_by
        a = flist(["apple", "banana", "pear", "kiwi"])
        sorted_by_len = a.sort_by(len)
        assert list(sorted_by_len) == ["pear", "kiwi", "apple", "banana"]
        
    # Edge cases tests
    def test_empty_list(self):
        """Test operations on empty list"""
        a = flist([])
        assert len(a) == 0
        assert list(a.map(lambda x: x * 2)) == []
        
        # Test partition on empty list
        assert list(a.partition_all(3)) == []
        
        # Test with operation that requires elements
        with pytest.raises((IndexError, StopIteration)):
            a.first()
            
    def test_large_list(self):
        """Test with a large list to ensure efficient operations"""
        a = frange(10000)
        assert len(a) == 10000
        assert a.first() == 0
        assert a.last() == 9999
        
        # Test efficient operations like take
        first_10 = a.take(10)
        assert len(first_10) == 10
        assert list(first_10) == list(range(10))