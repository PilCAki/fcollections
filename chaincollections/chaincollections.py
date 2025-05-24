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
    def _preserve_recursive(self, result):
        """Helper to preserve recursive behavior in results."""
        if hasattr(self, '_recursive') and self._recursive and isinstance(result, (clist, cdict)):
            result._recursive = True
        return result
    
    def map(self, f: Callable[[T], S]) -> 'CBase':
        """Map a function over the elements."""
        result = self.__class__(map(f, self))
        return self._preserve_recursive(result)
    
    def reduce(self, f: Callable[[T, T], T], initializer: Optional[T] = None) -> T:
        """Reduce the elements using a function."""
        return reduce(f, self, initializer) if initializer is not None else reduce(f, self)
    
    def concat(self) -> 'CBase':
        """Concatenate nested iterables."""
        result = self.__class__(cytoolz.concat(self))
        return self._preserve_recursive(result)
    
    def diff(self, *seqs: Iterable, **kwargs) -> 'CBase':
        """Return elements in self that are not in any of the sequences."""
        result = self.__class__(cytoolz.diff(*((self,)+seqs), **kwargs))
        return self._preserve_recursive(result)
    
    def drop(self, n: int) -> 'CBase':
        """Drop the first n elements."""
        result = self.__class__(cytoolz.drop(n, self))
        return self._preserve_recursive(result)
    
    def filter(self, predicate: Callable[[T], bool]) -> 'CBase':
        """Filter elements based on a predicate."""
        result = self.__class__(filter(predicate, self))
        return self._preserve_recursive(result)
    
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
## CLASSES
## --------------------------------------------------------------------------------

class clist(CBase, list):
    """Functional list class with chainable methods."""
    
    def __getitem__(self, key: Union[int, slice]) -> Union[T, 'clist']:
        """Get item at index or slice."""
        result = super(clist, self).__getitem__(key)
        
        # If this is a recursive collection and the result is a collection, wrap it
        if hasattr(self, '_recursive') and self._recursive:
            if isinstance(result, dict):
                recursive_result = cdict(result)
                recursive_result._recursive = True
                return recursive_result
            elif isinstance(result, list):
                recursive_result = clist(result)
                recursive_result._recursive = True
                return recursive_result
            
        # Handle slices by wrapping the result in a clist
        if isinstance(key, slice):
            return clist(result)
            
        return result
    
    def append(self, item: T) -> 'clist':
        """Append an item and return a new clist."""
        new_list = clist(self)
        super(clist, new_list).append(item)
        if hasattr(self, '_recursive') and self._recursive:
            new_list._recursive = True
        return new_list
    
    def sort(self, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> 'clist':
        """Sort the list and return a new clist."""
        result = clist(sorted(self, key=key, reverse=reverse))
        if hasattr(self, '_recursive') and self._recursive:
            result._recursive = True
        return result
    
    def reverse(self) -> 'clist':
        """Reverse the list and return a new clist."""
        result = clist(reversed(self))
        if hasattr(self, '_recursive') and self._recursive:
            result._recursive = True
        return result
    
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
    """Functional generator class with chainable methods."""
    
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
    """Functional dictionary class with chainable methods."""
    
    def __getitem__(self, key: K) -> V:
        """Get item by key with recursive chaining support."""
        result = super().__getitem__(key)
        
        # If this is a recursive collection and the result is a collection, wrap it
        if hasattr(self, '_recursive') and self._recursive:
            if isinstance(result, dict):
                recursive_result = cdict(result)
                recursive_result._recursive = True
                return recursive_result
            elif isinstance(result, list):
                recursive_result = clist(result)
                recursive_result._recursive = True
                return recursive_result
        
        return result
    
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
    """Functional set class with chainable methods."""
    
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
    """Range as a list."""
    return clist(range(*args))

def cxrange(*args: int) -> cgenerator:
    """Range as a generator."""
    return cgenerator(range(*args))

def chain(obj: Any, recursive: bool = False) -> Union[clist, cdict, cset, cgenerator]:
    """
    Convert any Python collection to its appropriate chaincollections type.
    
    Args:
        obj: Any Python object
        recursive: If True, any nested dict/list will be automatically wrapped as 
                  a chainable object when accessed. Default is False.
        
    Returns:
        The appropriate chaincollections type (clist, cdict, cset, or cgenerator)
    """
    # If it's already a chaincollections type, return it as is
    if isinstance(obj, (clist, cdict, cset, cgenerator)):
        if recursive and not getattr(obj, '_recursive', False):
            # If recursive is requested but the object isn't already recursive,
            # create a new recursive version
            if isinstance(obj, cdict):
                result = cdict(obj)
                result._recursive = True
                return result
            elif isinstance(obj, clist):
                result = clist(obj)
                result._recursive = True
                return result
            elif isinstance(obj, cset):
                # Sets don't need recursive behavior since their elements are not indexed
                return obj
            else:  # cgenerator
                # Generators don't need recursive behavior since their elements are accessed by iteration
                return obj
        return obj
    
    # Convert based on type
    if isinstance(obj, dict):
        result = cdict(obj)
        if recursive:
            result._recursive = True
        return result
    elif isinstance(obj, set):
        return cset(obj)
    elif isinstance(obj, list):
        result = clist(obj)
        if recursive:
            result._recursive = True
        return result
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
        # Handle other iterables as generators
        return cgenerator(obj)
    else:
        # For non-collections, wrap in a singleton list
        result = clist([obj])
        if recursive:
            result._recursive = True
        return result
