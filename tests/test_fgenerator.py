"""
Unit tests for fgenerator functionality
"""
import pytest
from chaincollections import fgenerator, fxrange, flist, fset

class TestFGenerator:
    def test_creation(self):
        """Test basic generator creation"""
        gen = fgenerator(range(5))
        assert isinstance(gen, fgenerator)
        # Converting to list to check content
        assert list(gen) == [0, 1, 2, 3, 4]
        
    def test_fxrange(self):
        """Test fxrange factory function"""
        gen = fxrange(5)
        assert isinstance(gen, fgenerator)
        assert list(gen) == [0, 1, 2, 3, 4]
        
        # Test with start, stop
        gen = fxrange(2, 7)
        assert list(gen) == [2, 3, 4, 5, 6]
        
        # Test with start, stop, step
        gen = fxrange(0, 10, 2)
        assert list(gen) == [0, 2, 4, 6, 8]
        
    def test_map(self):
        """Test mapping function over a generator"""
        gen = fxrange(5)
        result = gen.map(lambda x: x * 2)
        assert isinstance(result, fgenerator)
        assert list(result) == [0, 2, 4, 6, 8]
        
    def test_filter(self):
        """Test filtering elements"""
        gen = fxrange(10)
        result = gen.filter(lambda x: x % 2 == 0)  # Even numbers
        assert isinstance(result, fgenerator)
        assert list(result) == [0, 2, 4, 6, 8]
        
    def test_to_list(self):
        """Test conversion to list"""
        gen = fxrange(5)
        result = gen.to_list()
        assert isinstance(result, flist)
        assert list(result) == [0, 1, 2, 3, 4]
        
    def test_reduce(self):
        """Test reduce functionality"""
        gen = fxrange(5)
        result = gen.reduce(lambda a, b: a + b)
        assert result == 10
        
    def test_take_drop(self):
        """Test take and drop methods"""
        gen = fxrange(10)
        take_result = gen.take(3)
        assert list(take_result) == [0, 1, 2]
        
        gen = fxrange(10)  # Need to recreate as generators are consumed
        drop_result = gen.drop(7)
        assert list(drop_result) == [7, 8, 9]
        
    def test_partition(self):
        """Test partitioning elements"""
        gen = fxrange(10)
        result = gen.partition(3)
        assert [list(p) for p in result] == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        
        # Test partition_all (includes incomplete chunks)
        gen = fxrange(10)  # Recreate generator
        result = gen.partition_all(4)
        assert [list(p) for p in result] == [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
        
    def test_sliding_window(self):
        """Test sliding window functionality"""
        gen = fxrange(5)
        result = gen.sliding_window(3).to_list()
        assert len(result) == 3
        assert [list(w) for w in result] == [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
        
    def test_pipe(self):
        """Test pipe functionality"""
        gen = fxrange(5)
        result = gen.pipe(lambda x: [i * 2 for i in x], sum)
        assert result == 20  # sum of [0, 2, 4, 6, 8]
        
    def test_pipe_map(self):
        """Test pipe_map functionality"""
        gen = fxrange(5)
        result = gen.pipe_map(lambda x: x - 4, lambda x: x + 4, lambda x: x * 2)
        assert list(result) == [0, 2, 4, 6, 8]
    
    def test_new_methods(self):
        """Test new chainable methods"""
        # Find
        gen = fxrange(10)
        found = gen.find(lambda x: x > 5)
        assert found == 6
        
        # Not found
        gen = fxrange(10)
        not_found = gen.find(lambda x: x > 20)
        assert not_found is None
        
        # Zip with
        gen1 = fxrange(5)
        gen2 = fxrange(5, 10)
        zipped = gen1.zip_with(gen2, lambda x, y: x + y)
        assert isinstance(zipped, fgenerator)
        assert list(zipped) == [5, 7, 9, 11, 13]
        
        # Chunk (alias for partition)
        gen = fxrange(5)
        chunks = gen.chunk(2)
        assert isinstance(chunks, fgenerator)
        assert [list(c) for c in chunks] == [[0, 1], [2, 3]]
        
        # Flatten
        gen = fgenerator([[1, 2], [3, 4], [5, 6]])
        flattened = gen.flatten()
        assert isinstance(flattened, fgenerator)
        assert list(flattened) == [1, 2, 3, 4, 5, 6]
        
        # Any match / all match
        gen = fxrange(5)
        assert gen.any_match(lambda x: x > 3) is True
        
        gen = fxrange(5)
        assert gen.any_match(lambda x: x < 0) is False
        
        gen = fxrange(5)
        assert gen.all_match(lambda x: x >= 0) is True
        
        gen = fxrange(5)
        assert gen.all_match(lambda x: x > 2) is False
        
        # Enumerate
        gen = fxrange(5)
        enumerated = gen.enumerate(1)
        assert isinstance(enumerated, fgenerator)
        assert list(enumerated) == [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4)]
        
        # Take while / drop while
        gen = fxrange(10)
        taken = gen.take_while(lambda x: x < 5)
        assert isinstance(taken, fgenerator)
        assert list(taken) == [0, 1, 2, 3, 4]
        
        gen = fxrange(10)
        dropped = gen.drop_while(lambda x: x < 5)
        assert isinstance(dropped, fgenerator)
        assert list(dropped) == [5, 6, 7, 8, 9]
    
    def test_conversion_methods(self):
        """Test new conversion methods"""
        gen = fxrange(5)
        
        # To set
        s = gen.to_set()
        assert isinstance(s, fset)
        assert s == {0, 1, 2, 3, 4}
        
        # To tuple
        gen = fxrange(5)
        t = gen.to_tuple()
        assert isinstance(t, tuple)
        assert t == (0, 1, 2, 3, 4)
        
    def test_laziness(self):
        """Test that operations are lazy (not evaluated until needed)"""
        # Create a generator that would raise an error if fully consumed
        def problematic_generator():
            for i in range(5):
                yield i
            raise ValueError("Generator fully consumed")
            
        gen = fgenerator(problematic_generator())
        mapped = gen.map(lambda x: x * 2)
        filtered = mapped.filter(lambda x: x > 0)
        
        # Taking just the first two elements should not raise an error
        result = filtered.take(2)
        assert list(result) == [2, 4]
        
    # Edge cases tests
    def test_empty_generator(self):
        """Test operations on empty generator"""
        gen = fgenerator([])
        assert list(gen) == []
        assert list(gen.map(lambda x: x * 2)) == []
        
        # Test with operation that requires elements
        gen = fgenerator([])
        with pytest.raises((IndexError, StopIteration)):
            gen.first()
            
    def test_infinite_generator(self):
        """Test with a potentially infinite generator but limited consumption"""
        def count_forever():
            i = 0
            while True:
                yield i
                i += 1
                
        gen = fgenerator(count_forever())
        result = gen.take(5)
        assert list(result) == [0, 1, 2, 3, 4]