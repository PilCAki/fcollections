'''

chaincollections.py

Chainable collections with functional programming methods from cytoolz, itertools and more.

clist member functions always return clist if it makes sense.

cgenerator member functions always return cgenerator if it makes sense.

Exceptions are functions which should obviously return other types, like "reduce" - 
    which may return a whole host of types.

Converting between a list and a generator is done by using .to_list() or .to_generator()

.to_list() and .to_generator() can be used to ensure that something you MEAN to be a list
or generator stays and is that way.

clist() and cgenerator() can be used to convert any normal iterable to either

There's a cdict and cset too.

Note: For backwards compatibility, flist, fgenerator, fdict, fset, frange, and fxrange 
are still available as aliases.

'''

import cytoolz
import itertools
import toolz  # Added for functions not in cytoolz
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

class CBase:
    def map(self, f: Callable[[T], S]) -> 'CBase':
        """Map a function over the elements."""
        return self.__class__(map(f, self))
    
    def reduce(self, f: Callable[[T, T], T], initializer: Optional[T] = None) -> T:
        """Reduce the elements using a function."""
        return reduce(f, self, initializer) if initializer is not None else reduce(f, self)
    
    def concat(self) -> 'CBase':
        """Concatenate nested iterables."""
        return self.__class__(cytoolz.concat(self))
    
    def diff(self, *seqs: Iterable, **kwargs) -> 'CBase':
        """Return elements in self that are not in any of the sequences."""
        return self.__class__(cytoolz.diff(*((self,)+seqs), **kwargs))
    
    def drop(self, n: int) -> 'CBase':
        """Drop the first n elements."""
        return self.__class__(cytoolz.drop(n, self))
    
    def filter(self, predicate: Callable[[T], bool]) -> 'CBase':
        """Filter elements based on a predicate."""
        return self.__class__(filter(predicate, self))
    
    def first(self) -> T:
        """Return the first element."""
        return cytoolz.first(self)
    
    @property
    def frequencies(self) -> Dict:
        """Count occurrences of each element."""
        if isinstance(self, clist) or isinstance(self, cgenerator) or isinstance(self, cset):
            return cdict(cytoolz.frequencies(self))
        else:
            return fdict(cytoolz.frequencies(self))
    
    def groupby(self, key: Callable[[T], K]) -> Dict:
        """Group elements by a key function."""
        if isinstance(self, clist) or isinstance(self, cgenerator) or isinstance(self, cset):
            return cdict(cytoolz.groupby(key, self)).valmap(clist)
        else:
            return fdict(cytoolz.groupby(key, self)).valmap(flist)
    
    def interleave(self, seq: Iterable[T], swap: bool = False) -> 'CBase':
        """Interleave elements from two sequences."""
        args = (seq, self) if swap else (self, seq)
        return self.__class__(cytoolz.interleave(args))
    
    def interpose(self, el: T) -> 'CBase':
        """Insert an element between each item."""
        return self.__class__(cytoolz.interpose(el, self))
    
    @property
    def is_distinct(self) -> bool:
        """Check if all elements are unique."""
        return cytoolz.isdistinct(self)
    
    def join(self, rightseq: Iterable, leftkey: Callable, rightkey: Callable) -> 'CBase':
        """Join two sequences based on matching keys."""
        return self.__class__(cytoolz.join(leftkey, self, rightkey, rightseq))
    
    def last(self) -> T:
        """Return the last element."""
        return cytoolz.last(self)

    def mapcat(self, f: Callable[[T], Iterable[S]]) -> 'CBase':
        """Map a function over elements and concatenate results."""
        return self.__class__(self.__class__(_.map(f) for _ in self)).concat()
    
    def nth(self, n: int) -> T:
        """Return the nth element."""
        return cytoolz.nth(n, self)
    
    def partition(self, n: int) -> 'CBase':
        """Partition sequence into tuples of length n."""
        return self.__class__(self.__class__(p) for p in cytoolz.partition(n, self))
    
    def partition_all(self, n: int) -> 'CBase':
        """Partition sequence into tuples of length n, padding with None if needed."""
        return self.__class__(self.__class__(p) for p in cytoolz.partition_all(n, self))
    
    def peek(self) -> T:
        """Look at first element and return a new iterator."""
        first, seq = cytoolz.peek(self)
        self = self.__class__(seq)
        return first
    
    def pluck(self, ind: Union[int, Iterable[int]]) -> 'CBase':
        """Extract values at the given indices from each element."""
        if cytoolz.isiterable(ind):
            if isinstance(self, clist) or isinstance(self, cgenerator) or isinstance(self, cset):
                return self.__class__(map(clist, cytoolz.pluck(ind, self)))
            else:
                return self.__class__(map(flist, cytoolz.pluck(ind, self)))
        else:
            return self.__class__(cytoolz.pluck(ind, self))
    
    def reduce_by(self, key: Callable[[T], K], op: Callable[[S, T], S]) -> Dict:
        """Group elements by key and reduce each group with a binary operator."""
        if isinstance(self, clist) or isinstance(self, cgenerator) or isinstance(self, cset):
            return cdict(cytoolz.reduceby(key, op, self))
        else:
            return fdict(cytoolz.reduceby(key, op, self))
    
    def remove(self, predicate: Callable[[T], bool]) -> 'CBase':
        """Remove elements that satisfy the predicate."""
        return self.__class__(cytoolz.remove(predicate, self))
    
    def second(self) -> T:
        """Return the second element."""
        return cytoolz.second(self)
    
    def sliding_window(self, n: int) -> Iterable:
        """Create a sliding window of elements."""
        # assuming should always be a generator - otherwise - going to get huge
        if isinstance(self, clist) or isinstance(self, cgenerator) or isinstance(self, cset):
            return cgenerator(self.__class__(sw) for sw in cytoolz.sliding_window(n, self))
        else:
            return fgenerator(self.__class__(sw) for sw in cytoolz.sliding_window(n, self))
    
    def take(self, n: int) -> 'CBase':
        """Take the first n elements."""
        return self.__class__(cytoolz.take(n, self))
    
    def tail(self, n: int) -> 'CBase':
        """Take the last n elements."""
        return self.__class__(cytoolz.tail(n, self))
    
    def stride_by(self, n: int) -> 'CBase':
        """Take every nth element."""
        # is "take_nth" in cytoolz, which just isn't a good name for what it actually does
        return self.__class__(cytoolz.take_nth(n, self)) 
    def top_k(self, k: int, key: Callable[[T], Any] = cytoolz.functoolz.identity) -> 'CBase':
        """Return the k largest elements."""
        return self.__class__(cytoolz.topk(k, self, key))
    
    def unique(self, key: Callable[[T], K] = cytoolz.functoolz.identity) -> 'CBase':
        """Return only unique elements."""
        return self.__class__(cytoolz.unique(self, key))
    
    def count_by(self, key: Callable[[T], K] = cytoolz.functoolz.identity) -> Dict:
        """Count occurrences of each key."""
        if isinstance(self, clist) or isinstance(self, cgenerator) or isinstance(self, cset):
            return cdict(cytoolz.countby(key, self))
        else:
            return fdict(cytoolz.countby(key, self))
    
    def partition_by(self, f: Callable[[T], Any]) -> 'CBase':
        """Partition a sequence based on result of a function."""
        return self.__class__(self.__class__(p) for p in cytoolz.partitionby(f, self))
    
    def pipe(self, *fs: Callable) -> Any:
        """Apply a sequence of functions to the data."""
        return cytoolz.functoolz.pipe(self, *fs)
    
    def pipe_map(self, *fs: Callable) -> 'CBase':
        """Apply a sequence of functions to each element."""
        return self.__class__(cytoolz.functoolz.pipe(_, *fs) for _ in self)
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Find first element that satisfies predicate, or None if not found."""
        for item in self:
            if predicate(item):
                return item
        return None
    
    def zip_with(self, seq: Iterable, func: Callable[[T, Any], S]) -> 'CBase':
        """Combine two sequences using a function."""
        return self.__class__(func(a, b) for a, b in zip(self, seq))
    
    def chunk(self, n: int) -> 'CBase':
        """Alias for partition with more intuitive name."""
        return self.partition(n)
    
    def flatten(self) -> 'CBase':
        """Flatten one level of nesting."""
        return self.__class__(item for sublist in self for item in sublist)
    
    def any_match(self, predicate: Callable[[T], bool]) -> bool:
        """Return True if any element satisfies the predicate."""
        return any(predicate(x) for x in self)
    
    def all_match(self, predicate: Callable[[T], bool]) -> bool:
        """Return True if all elements satisfy the predicate."""
        return all(predicate(x) for x in self)
    
    def enumerate(self, start: int = 0) -> 'CBase':
        """Return (index, item) pairs."""
        return self.__class__(enumerate(self, start))
    
    def take_while(self, predicate: Callable[[T], bool]) -> 'CBase':
        """Take elements while predicate is true."""
        def _take_while():
            for element in self:
                if predicate(element):
                    yield element
                else:
                    break
        return self.__class__(_take_while())
    
    def drop_while(self, predicate: Callable[[T], bool]) -> 'CBase':
        """Drop elements while predicate is true."""
        def _drop_while():
            dropping = True
            for element in self:
                if dropping and not predicate(element):
                    dropping = False
                if not dropping:
                    yield element
        return self.__class__(_drop_while())
    
## --------------------------------------------------------------------------------
## MAIN CLASSES
## --------------------------------------------------------------------------------

class flist(CBase, list):
    def __getitem__(self, key: Union[int, slice]) -> Union[T, 'flist']:
        """Get item at index or slice."""
        result = super(flist, self).__getitem__(key)
        if isinstance(key, slice):
            return flist(result)
        return result
    
    def to_generator(self) -> 'fgenerator':
        """Convert list to generator."""
        return fgenerator(self)
    
    def to_set(self) -> 'fset':
        """Convert list to set."""
        return fset(self)
    
    def to_tuple(self) -> tuple:
        """Convert list to tuple."""
        return tuple(self)
    
    def sort(self) -> 'flist':
        """Return a sorted list."""
        return self.__class__(sorted(self))
    
    def sort_by(self, key: Callable[[T], Any]) -> 'flist':
        """Return a list sorted by key function."""
        return self.__class__(sorted(self, key=key))

class fgenerator(CBase):
    def __init__(self, _iterable: Iterable[T]):
        self._iterable = _iterable
    
    def __iter__(self) -> Generator[T, None, None]:
        return (_ for _ in self._iterable)
    
    def to_list(self) -> flist:
        """Convert generator to list."""
        return flist(self)
    
    def to_set(self) -> 'fset':
        """Convert generator to set."""
        return fset(self)
    
    def to_tuple(self) -> tuple:
        """Convert generator to tuple."""
        return tuple(self)
    
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
    
    def to_pairs(self) -> flist:
        """Convert dictionary to list of key-value pairs."""
        return flist(self.items())
    
    @classmethod
    def from_pairs(cls, pairs: Iterable[Tuple[K, V]]) -> 'fdict':
        """Create dictionary from list of key-value pairs."""
        return cls(pairs)

class fset(CBase, set):
    """Functional set class with chainable methods."""
    
    def to_list(self) -> flist:
        """Convert set to list."""
        return flist(self)
    
    def to_generator(self) -> fgenerator:
        """Convert set to generator."""
        return fgenerator(self)
    
    def to_tuple(self) -> tuple:
        """Convert set to tuple."""
        return tuple(self)
        
    def union(self, *others: Iterable) -> 'fset':
        """Return union of sets."""
        return fset(super().union(*others))
    
    def intersection(self, *others: Iterable) -> 'fset':
        """Return intersection of sets."""
        return fset(super().intersection(*others))
    
    def difference(self, *others: Iterable) -> 'fset':
        """Return difference of sets."""
        return fset(super().difference(*others))
    
    def symmetric_difference(self, other: Iterable) -> 'fset':
        """Return symmetric difference of sets."""
        return fset(super().symmetric_difference(other))
    
def frange(*args: int) -> flist:
    """Range as a list."""
    return flist(range(*args))

def fxrange(*args: int) -> fgenerator:
    """Range as a generator."""
    return fgenerator(range(*args))


## --------------------------------------------------------------------------------
## NEW CHAINCOLLECTIONS API CLASSES
## --------------------------------------------------------------------------------

class clist(CBase, list):
    """Functional list class with chainable methods - chaincollections API."""
    
    def __getitem__(self, key: Union[int, slice]) -> Union[T, 'clist']:
        """Get item at index or slice."""
        result = super(clist, self).__getitem__(key)
        if isinstance(key, slice):
            return clist(result)
        return result
    
    def append(self, item: T) -> 'clist':
        """Append an item and return a new clist."""
        new_list = clist(self)
        super(clist, new_list).append(item)
        return new_list
    
    def sort(self, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> 'clist':
        """Sort the list and return a new clist."""
        return clist(sorted(self, key=key, reverse=reverse))
    
    def reverse(self) -> 'clist':
        """Reverse the list and return a new clist."""
        return clist(reversed(self))
    
    def to_generator(self) -> 'cgenerator':
        """Convert list to generator."""
        return cgenerator(self)
    
    def to_set(self) -> 'cset':
        """Convert list to set."""
        return cset(self)
    
    def to_dict(self) -> 'cdict':
        """Convert list of pairs to dict."""
        return cdict(self)

class cgenerator(CBase):
    """Functional generator class with chainable methods - chaincollections API."""
    
    def __init__(self, iterable: Iterable[T]):
        """Initialize generator from iterable."""
        self.iterable = iterable

    def __iter__(self):
        """Return iterator over the iterable."""
        return iter(self.iterable)
    
    def __getitem__(self, key: Union[int, slice]) -> Union[T, 'cgenerator']:
        """Convert to list first, then get item."""
        as_list = list(self)
        result = as_list[key]
        if isinstance(key, slice):
            return cgenerator(result)
        return result
    
    def to_list(self) -> clist:
        """Convert generator to list."""
        return clist(self)
    
    def to_set(self) -> 'cset':
        """Convert generator to set."""
        return cset(self)
    
    def to_dict(self) -> 'cdict':
        """Convert generator of pairs to dict."""
        return cdict(self)

class cdict(dict):
    """Functional dictionary class with chainable methods - chaincollections API."""
    
    def keys(self) -> clist:
        """Return keys as clist."""
        return clist(super().keys())
    
    def values(self) -> clist:
        """Return values as clist."""
        return clist(super().values())
    
    def items(self) -> clist:
        """Return items as clist."""
        return clist(super().items())
    
    def keymap(self, f: Callable[[K], S]) -> 'cdict':
        """Map function over keys."""
        return cdict(cytoolz.keymap(f, self))
    
    def valmap(self, f: Callable[[V], S]) -> 'cdict':
        """Map function over values."""
        return cdict(cytoolz.valmap(f, self))
    
    def itemmap(self, f: Callable[[Tuple[K, V]], Tuple[S, U]]) -> cgenerator:
        """Map function over items."""
        return cgenerator(cytoolz.itemmap(f, self))
    
    def keyfilter(self, predicate: Callable[[K], bool]) -> 'cdict':
        """Filter keys by predicate."""
        return cdict(cytoolz.keyfilter(predicate, self))
    
    def valfilter(self, predicate: Callable[[V], bool]) -> 'cdict':
        """Filter values by predicate."""
        return cdict(cytoolz.valfilter(predicate, self))
    
    def itemfilter(self, predicate: Callable[[Tuple[K, V]], bool]) -> 'cdict':
        """Filter items by predicate."""
        return cdict(cytoolz.itemfilter(predicate, self))
    
    def merge(self, *dicts: Dict, **kwargs) -> 'cdict':
        """Merge with other dictionaries."""
        return cdict(cytoolz.merge(*((self,) + dicts), **kwargs))

class cset(CBase, set):
    """Functional set class with chainable methods - chaincollections API."""
    
    def to_list(self) -> clist:
        """Convert set to list."""
        return clist(self)
    
    def to_generator(self) -> cgenerator:
        """Convert set to generator."""
        return cgenerator(self)
    
    def to_tuple(self) -> tuple:
        """Convert set to tuple."""
        return tuple(self)
        
    def union(self, *others: Iterable) -> 'cset':
        """Return union of sets."""
        return cset(super().union(*others))
    
    def intersection(self, *others: Iterable) -> 'cset':
        """Return intersection of sets."""
        return cset(super().intersection(*others))
    
    def difference(self, *others: Iterable) -> 'cset':
        """Return difference of sets."""
        return cset(super().difference(*others))
    
    def symmetric_difference(self, other: Iterable) -> 'cset':
        """Return symmetric difference of sets."""
        return cset(super().symmetric_difference(other))

def crange(*args: int) -> clist:
    """Range as a list - chaincollections API."""
    return clist(range(*args))

def cxrange(*args: int) -> cgenerator:
    """Range as a generator - chaincollections API."""
    return cgenerator(range(*args))


## --------------------------------------------------------------------------------
## BACKWARDS COMPATIBILITY ALIASES
## --------------------------------------------------------------------------------

# Maintain backwards compatibility with old fcollections names
FBase = CBase  # Alias for backwards compatibility
