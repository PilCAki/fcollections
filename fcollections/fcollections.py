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

There's an fdict and fset too.
'''

import cytoolz
import itertools
import sys

# Python 2/3 compatibility
PY2 = sys.version_info[0] == 2

if PY2:
    from itertools import imap, ifilter
    range = xrange
    reduce_func = reduce
else:
    from functools import reduce as reduce_func
    imap = map
    ifilter = filter
    range = range

## --------------------------------------------------------------------------------
## BASE CLASS
## --------------------------------------------------------------------------------

class FBase(object):
    def map(self, f):
        return self.__class__(imap(f, self))
    def reduce(self, f, initializer=None):
        return reduce_func(f, self, initializer) if initializer else reduce_func(f, self)
    def concat(self):
        return self.__class__(cytoolz.concat(self))
    def diff(self, *seqs, **kwargs):
        return self.__class__(cytoolz.diff(*((self,)+seqs), **kwargs))
    def drop(self, n):
        return self.__class__(cytoolz.drop(n, self))
    def filter(self, predicate):
        return self.__class__(ifilter(predicate, self))
    def first(self):
        return cytoolz.first(self)
    def frequencies(self):
        return fdict(cytoolz.frequencies(self))
    def groupby(self, key):
        return fdict(cytoolz.groupby(key, self)).valmap(flist)
    def accumulate(self, binop, initial=None):
        ''' Return accumulated results of binary operation
            Similar to reduce but keeps intermediate results '''
        if initial is None:
            # No initial value
            result = []
            iterator = iter(self)
            try:
                acc = next(iterator)
                result.append(acc)
                for item in iterator:
                    acc = binop(acc, item)
                    result.append(acc)
                return self.__class__(result)
            except StopIteration:
                return self.__class__([])
        else:
            # Initial value provided
            result = [initial]
            acc = initial
            for item in self:
                acc = binop(acc, item)
                result.append(acc)
            return self.__class__(result[1:])  # Skip the initial value in the result
    def interleave(self, seq, swap=False):
        args = (seq, self) if swap else (self, seq)
        return self.__class__(cytoolz.interleave(args))
    def interpose(self, el):
        return self.__class__(cytoolz.interpose(el, self))
    def is_distinct(self):
        return cytoolz.isdistinct(self)
    def join(self, rightseq, leftkey, rightkey):
        return self.__class__(cytoolz.join(leftkey, self, rightkey, rightseq))
    def last(self):
        return cytoolz.last(self)
    def mapcat(self, f):
        return self.__class__(_.map(f) for _ in self).concat
    def nth(self, n):
        return cytoolz.nth(n, self)
    def partition(self, n):
        return self.__class__(self.__class__(p) for p in cytoolz.partition(n, self))
    def partition_all(self, n):
        return self.__class__(self.__class__(p) for p in cytoolz.partition_all(n, self))
    def peek(self):
        first, seq = cytoolz.peek(self)
        self = self.__class__(seq)
        return first
    def pluck(self, ind):
        if cytoolz.isiterable(ind): return self.__class__(imap(flist, cytoolz.pluck(ind, self)))
        else: return self.__class__(cytoolz.pluck(ind, self))
    def reduce_by(self, key, op):
        return fdict(cytoolz.reduceby(key, op, self)) 
    def remove(self, predicate):
        return self.__class__(cytoolz.remove(predicate, self))
    def second(self):
        return cytoolz.second(self)
    def sliding_window(self, n):
        ''' assuming should always be a generator - otherwise - going to get huge '''
        return fgenerator(self.__class__(sw) for sw in cytoolz.sliding_window(n, self))
    def take(self, n):
        return self.__class__(cytoolz.take(n, self))
    def tail(self, n):
        return self.__class__(cytoolz.tail(n, self))
    def stride_by(self, n):
        ''' is "take_nth" in cytoolz, which just isn't a good name for what it actually does '''
        return self.__class__(cytoolz.take_nth(n, self)) 
    def top_k(self, k, key=cytoolz.functoolz.identity):
        return self.__class__(cytoolz.topk(k, self, key))
    def unique(self, key=cytoolz.functoolz.identity):
        return self.__class__(cytoolz.unique(self, key))
    def count_by(self, key=cytoolz.functoolz.identity):
        return fdict(cytoolz.countby(key, self))
    def partition_by(self, f):
        return self.__class__(self.__class__(p) for p in cytoolz.partitionby(f, self))
    def pipe(self, *fs):
        return cytoolz.functoolz.pipe(self, *fs) 
    def pipe_map(self, *fs):
        return self.__class__(cytoolz.functoolz.pipe(x, *fs) for x in self)
    def flatten(self, depth=1):
        ''' Flatten nested iterables
            depth: number of levels to flatten (default: 1) '''
        result = self
        for _ in range(depth):
            result = self.__class__(cytoolz.concat(result))
        return result
    def chunk(self, n):
        ''' Break iterable into chunks of size n
            Similar to partition but doesn't drop incomplete final chunk '''
        return self.__class__(self.__class__(ch) for ch in cytoolz.partition_all(n, self))
    def zip_with(self, func, *seqs):
        ''' Zip together multiple sequences and apply function
            Returns same collection type with results of func(x, y, z, ...) '''
        if PY2:
            return self.__class__(itertools.starmap(func, itertools.izip(self, *seqs)))
        else:
            return self.__class__(itertools.starmap(func, zip(self, *seqs)))
    def do(self, func):
        ''' Apply function to data and return original data
            Useful for side effects like logging/printing
            Example: frange(5).do(print).map(lambda x: x*2) '''
        for item in self:
            func(item)
        return self
    
## --------------------------------------------------------------------------------
## MAIN CLASSES
## --------------------------------------------------------------------------------

class flist(FBase, list):
    def __getslice__(self, *args):
        return flist(super(flist, self).__getslice__(*args))
    def to_generator(self):
        return fgenerator(self)
    def sort(self):
        return self.__class__(sorted(self))
    def sort_by(self, key):
        return self.__class__(sorted(self, key=key))

class fgenerator(FBase):
    def __init__(self, _iterable):
        self._iterable = _iterable
    def __iter__(self):
        return (_ for _ in self._iterable)
    def to_list(self):
        return flist(self)
    def get(self, ind, default=None):
        return cytoolz.get(ind, self, default)
    
class fset(FBase, set):
    ''' Functional set with chaining support '''
    def __init__(self, iterable=None):
        iterable = iterable or []
        super(fset, self).__init__(iterable) 
    def union(self, other):
        return fset(super(fset, self).union(other))
    def intersection(self, other):
        return fset(super(fset, self).intersection(other))
    def difference(self, other):
        return fset(super(fset, self).difference(other))
    def symmetric_difference(self, other):
        return fset(super(fset, self).symmetric_difference(other))
    def issubset(self, other):
        return super(fset, self).issubset(other)
    def issuperset(self, other):
        return super(fset, self).issuperset(other)
    def to_list(self):
        return flist(self)
    def to_generator(self):
        return fgenerator(self)
    
class fdict(dict):
    # Use simple dict methods to avoid property issues
    def get_keys(self):
        return flist(dict.keys(self))
    
    def get_values(self):
        return flist(dict.values(self))
    
    def get_items(self):
        return flist(dict.items(self))
    
    def keymap(self, f):
        return fdict(cytoolz.keymap(f, self))
    def valmap(self, f):
        return fdict(cytoolz.valmap(f, self))
    def itemmap(self, f):
        return fgenerator(cytoolz.itemmap(f, self))
    def keyfilter(self, predicate):
        return fdict(cytoolz.keyfilter(predicate, self))
    def valfilter(self, predicate):
        return fdict(cytoolz.valfilter(predicate, self))
    def itemfilter(self, predicate):
        return fdict(cytoolz.itemfilter(predicate, self))
    def merge(self, *dicts, **kwargs):
        return fdict(cytoolz.merge(*((self,)+dicts), **kwargs))
    def merge_with(self, func, *dicts):
        ''' Merge dictionaries by combining values with given function
            Example: d1.merge_with(sum, d2, d3) '''
        # Create a manually merged dict to avoid recursion issues with cytoolz
        result = {}
        all_dicts = [self] + list(dicts)
        
        # Get all keys from all dictionaries
        all_keys = set()
        for d in all_dicts:
            all_keys.update(d.keys())
        
        for key in all_keys:
            values = []
            for d in all_dicts:
                if key in d:
                    values.append(d[key])
            
            if len(values) == 1:
                result[key] = values[0]
            else:
                result[key] = func(*values)
                
        return fdict(result)
        
    def assoc(self, *args):
        ''' Create new dict with given key-value pairs added '''
        if len(args) % 2 != 0:
            raise ValueError("assoc expects even number of arguments (key-value pairs)")
        result = self.copy()
        for i in range(0, len(args), 2):
            result[args[i]] = args[i+1]
        return fdict(result)
    def dissoc(self, *keys):
        ''' Create new dict with given keys removed '''
        result = self.copy()
        for key in keys:
            if key in result:
                del result[key]
        return fdict(result)
    def get_in(self, keys, default=None):
        ''' Access nested dictionary data by sequence of keys '''
        return cytoolz.get_in(keys, self, default=default)
    def assoc(self, *args):
        ''' Create new dict with given key-value pairs added '''
        if len(args) % 2 != 0:
            raise ValueError("assoc expects even number of arguments (key-value pairs)")
        result = self.copy()
        for i in range(0, len(args), 2):
            result[args[i]] = args[i+1]
        return fdict(result)
    def dissoc(self, *keys):
        ''' Create new dict with given keys removed '''
        result = self.copy()
        for key in keys:
            if key in result:
                del result[key]
        return fdict(result)
    def get_in(self, keys, default=None):
        ''' Access nested dictionary data by sequence of keys '''
        return cytoolz.get_in(keys, self, default=default)

def frange(*args):
    return flist(range(*args))
def fxrange(*args):
    return fgenerator(range(*args))

## --------------------------------------------------------------------------------
## UTILITY FUNCTIONS
## --------------------------------------------------------------------------------

def from_numpy(array):
    ''' Convert numpy array to flist '''
    return flist(array.tolist())

def to_numpy(fcollection):
    ''' Convert fcollection to numpy array '''
    import numpy as np
    return np.array(list(fcollection))

def from_pandas(df_or_series):
    ''' Convert pandas DataFrame or Series to fdict or flist '''
    if hasattr(df_or_series, 'to_dict'):
        if hasattr(df_or_series, 'columns'):
            # DataFrame
            return fdict({col: flist(df_or_series[col]) for col in df_or_series.columns})
        else:
            # Series
            return flist(df_or_series.values)
    raise TypeError("Expected pandas DataFrame or Series")

def to_pandas(fcollection):
    ''' Convert fcollection to pandas DataFrame '''
    import pandas as pd
    if isinstance(fcollection, fdict):
        return pd.DataFrame(dict(fcollection))
    return pd.Series(list(fcollection))
