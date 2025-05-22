'''

fcollections.py

tossing all the neat stuff from cytoolz and itertools and more in as members of collections classes.

flist member functions always return FList if it makes sense.

fgenerator member functions always return FGnenerator if it makes sense.

Exceptions are functions which should obviously return other types, like "reduce" - 
    which may return a whole host of types.

Converting between a list and a generator is done by using .tolist or .togenerator

.tolist and .togenerator can be used to ensure that something you MEAN to be a list
or generator stays and is that way.

flist() and fgenerator() can be used to convert any normal iterable to either

There's an fdict too.

'''

import cytoolz
import itertools
from typing import Any, Callable, Dict, Generator, Iterable, List, Optional, Tuple, TypeVar, Union, cast
from functools import reduce

# Type variables for generic functions
T = TypeVar('T')
S = TypeVar('S')
U = TypeVar('U')
K = TypeVar('K')
V = TypeVar('V')

## --------------------------------------------------------------------------------
## BASE CLASS
## --------------------------------------------------------------------------------

class FBase:
    def map(self, f: Callable[[T], S]) -> 'FBase':
        """Map a function over the elements."""
        return self.__class__(map(f, self))
    
    def reduce(self, f: Callable[[T, T], T], initializer: Optional[T] = None) -> T:
        """Reduce the elements using a function."""
        return reduce(f, self, initializer) if initializer is not None else reduce(f, self)
    
    def concat(self) -> 'FBase':
        """Concatenate nested iterables."""
        return self.__class__(cytoolz.concat(self))
    
    def diff(self, *seqs: Iterable, **kwargs) -> 'FBase':
        """Return elements in self that are not in any of the sequences."""
        return self.__class__(cytoolz.diff(*((self,)+seqs), **kwargs))
    
    def drop(self, n: int) -> 'FBase':
        """Drop the first n elements."""
        return self.__class__(cytoolz.drop(n, self))
    
    def filter(self, predicate: Callable[[T], bool]) -> 'FBase':
        """Filter elements based on a predicate."""
        return self.__class__(filter(predicate, self))
    
    @property
    def first(self) -> T:
        """Return the first element."""
        return cytoolz.first(self)
    
    @property
    def frequencies(self) -> 'fdict':
        """Count occurrences of each element."""
        return fdict(cytoolz.frequencies(self))
    
    def groupby(self, key: Callable[[T], K]) -> 'fdict':
        """Group elements by a key function."""
        return fdict(cytoolz.groupby(key, self)).valmap(flist)
    
    def interleave(self, seq: Iterable[T], swap: bool = False) -> 'FBase':
        """Interleave elements from two sequences."""
        args = (seq, self) if swap else (self, seq)
        return self.__class__(cytoolz.interleave(args))
    
    def interpose(self, el: T) -> 'FBase':
        """Insert an element between each item."""
        return self.__class__(cytoolz.interpose(el, self))
    
    @property
    def is_distinct(self) -> bool:
        """Check if all elements are unique."""
        return cytoolz.isdistinct(self)
    
    def join(self, rightseq: Iterable, leftkey: Callable, rightkey: Callable) -> 'FBase':
        """Join two sequences based on matching keys."""
        return self.__class__(cytoolz.join(leftkey, self, rightkey, rightseq))
    
    @property
    def last(self) -> T:
        """Return the last element."""
        return cytoolz.last(self)
    def mapcat(self, f: Callable[[T], Iterable[S]]) -> 'FBase':
        """Map a function over elements and concatenate results."""
        return self.__class__(self.__class__(_.map(f) for _ in self)).concat()
    
    def nth(self, n: int) -> T:
        """Return the nth element."""
        return cytoolz.nth(n, self)
    
    def partition(self, n: int) -> 'FBase':
        """Partition sequence into tuples of length n."""
        return self.__class__(self.__class__(p) for p in cytoolz.partition(n, self))
    
    def partition_all(self, n: int) -> 'FBase':
        """Partition sequence into tuples of length n, padding with None if needed."""
        return self.__class__(self.__class__(p) for p in cytoolz.partition_all(n, self))
    
    def peek(self) -> T:
        """Look at first element and return a new iterator."""
        first, seq = cytoolz.peek(self)
        self = self.__class__(seq)
        return first
    
    def pluck(self, ind: Union[int, Iterable[int]]) -> 'FBase':
        """Extract values at the given indices from each element."""
        if cytoolz.isiterable(ind):
            return self.__class__(map(flist, cytoolz.pluck(ind, self)))
        else:
            return self.__class__(cytoolz.pluck(ind, self))
    
    def reduce_by(self, key: Callable[[T], K], op: Callable[[S, T], S]) -> 'fdict':
        """Group elements by key and reduce each group with a binary operator."""
        return fdict(cytoolz.reduceby(key, op, self))
    
    def remove(self, predicate: Callable[[T], bool]) -> 'FBase':
        """Remove elements that satisfy the predicate."""
        return self.__class__(cytoolz.remove(predicate, self))
    
    @property
    def second(self) -> T:
        """Return the second element."""
        return cytoolz.second(self)
    
    def sliding_window(self, n: int) -> 'fgenerator':
        """Create a sliding window of elements."""
        # assuming should always be a generator - otherwise - going to get huge
        return fgenerator(self.__class__(sw) for sw in cytoolz.sliding_window(n, self))
    
    def take(self, n: int) -> 'FBase':
        """Take the first n elements."""
        return self.__class__(cytoolz.take(n, self))
    
    def tail(self, n: int) -> 'FBase':
        """Take the last n elements."""
        return self.__class__(cytoolz.tail(n, self))
    
    def stride_by(self, n: int) -> 'FBase':
        """Take every nth element."""
        # is "take_nth" in cytoolz, which just isn't a good name for what it actually does
        return self.__class__(cytoolz.take_nth(n, self)) 
    def top_k(self, k: int, key: Callable[[T], Any] = cytoolz.functoolz.identity) -> 'FBase':
        """Return the k largest elements."""
        return self.__class__(cytoolz.topk(k, self, key))
    
    def unique(self, key: Callable[[T], K] = cytoolz.functoolz.identity) -> 'FBase':
        """Return only unique elements."""
        return self.__class__(cytoolz.unique(self, key))
    
    def count_by(self, key: Callable[[T], K] = cytoolz.functoolz.identity) -> 'fdict':
        """Count occurrences of each key."""
        return fdict(cytoolz.countby(key, self))
    
    def partition_by(self, f: Callable[[T], Any]) -> 'FBase':
        """Partition a sequence based on result of a function."""
        return self.__class__(self.__class__(p) for p in cytoolz.partitionby(f, self))
    
    def pipe(self, *fs: Callable) -> Any:
        """Apply a sequence of functions to the data."""
        return cytoolz.functoolz.pipe(self, *fs)
    
    def pipe_map(self, *fs: Callable) -> 'FBase':
        """Apply a sequence of functions to each element."""
        return self.__class__(cytoolz.functoolz.pipe(_, *fs) for _ in self)
    
## --------------------------------------------------------------------------------
## MAIN CLASSES
## --------------------------------------------------------------------------------

class flist(FBase, list):
    def __getitem__(self, key: Union[int, slice]) -> Union[T, 'flist']:
        """Get item at index or slice."""
        result = super(flist, self).__getitem__(key)
        if isinstance(key, slice):
            return flist(result)
        return result
    
    def to_generator(self) -> 'fgenerator':
        """Convert list to generator."""
        return fgenerator(self)
    
    def sort(self) -> 'flist':
        """Return a sorted list."""
        return self.__class__(sorted(self))
    
    def sort_by(self, key: Callable[[T], Any]) -> 'flist':
        """Return a list sorted by key function."""
        return self.__class__(sorted(self, key=key))

class fgenerator(FBase):
    def __init__(self, _iterable: Iterable[T]):
        self._iterable = _iterable
    
    def __iter__(self) -> Generator[T, None, None]:
        return (_ for _ in self._iterable)
    
    def to_list(self) -> flist:
        """Convert generator to list."""
        return flist(self)
    
    def get(self, ind: int, default: Any = None) -> Any:
        """Get item at index or return default."""
        return cytoolz.get(ind, self, default)
    
class fdict(dict):
    def keys(self) -> flist:
        """Return list of keys."""
        return flist(super().keys())
    
    def values(self) -> flist:
        """Return list of values."""
        return flist(super().values())
    
    def items(self) -> flist:
        """Return list of items."""
        return flist(super().items())
    
    def keymap(self, f: Callable[[K], S]) -> 'fdict':
        """Apply function to keys."""
        return fdict(cytoolz.keymap(f, self))
    
    def valmap(self, f: Callable[[V], S]) -> 'fdict':
        """Apply function to values."""
        return fdict(cytoolz.valmap(f, self))
    
    def itemmap(self, f: Callable[[Tuple[K, V]], Tuple[S, U]]) -> 'fgenerator':
        """Apply function to items."""
        return fgenerator(cytoolz.itemmap(f, self))
    
    def keyfilter(self, predicate: Callable[[K], bool]) -> 'fdict':
        """Filter by key predicate."""
        return fdict(cytoolz.keyfilter(predicate, self))
    
    def valfilter(self, predicate: Callable[[V], bool]) -> 'fdict':
        """Filter by value predicate."""
        return fdict(cytoolz.valfilter(predicate, self))
    
    def itemfilter(self, predicate: Callable[[Tuple[K, V]], bool]) -> 'fdict':
        """Filter by item predicate."""
        return fdict(cytoolz.itemfilter(predicate, self))
    
    def merge(self, *dicts: dict, **kwargs) -> 'fdict':
        """Merge dictionaries."""
        return fdict(cytoolz.merge(*((self,)+dicts), **kwargs))

def frange(*args: int) -> flist:
    """Range as a list."""
    return flist(range(*args))

def fxrange(*args: int) -> fgenerator:
    """Range as a generator."""
    return fgenerator(range(*args))
