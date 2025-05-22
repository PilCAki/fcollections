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
import functools

## --------------------------------------------------------------------------------
## BASE CLASS
## --------------------------------------------------------------------------------

class FBase(object):
    def map(self, f):
        return self.__class__(map(f, self))
    def reduce(self, f, initializer=None):
        return functools.reduce(f, self, initializer) if initializer is not None else functools.reduce(f, self)
    def concat(self):
        return self.__class__(cytoolz.concat(self))
    def diff(self, *seqs, **kwargs):
        return self.__class__(cytoolz.diff(*((self,)+seqs), **kwargs))
    def drop(self, n):
        return self.__class__(cytoolz.drop(n, self))
    def filter(self, predicate):
        return self.__class__(filter(predicate, self))
    def first(self):
        return cytoolz.first(self)
    def frequencies(self):
        return fdict(cytoolz.frequencies(self))
    def groupby(self, key):
        return fdict(cytoolz.groupby(key, self)).valmap(flist)
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
        return self.__class__(_.map(f) for _ in self).concat()
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
        if cytoolz.isiterable(ind): return self.__class__(map(flist, cytoolz.pluck(ind, self)))
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
        return self.__class__(cytoolz.functoolz.pipe(_, *fs) for _ in self)
    
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
    
class fdict(dict):
    def keys(self):
        return flist(super().keys())
    def values(self):
        return flist(super().values())
    def items(self):
        return flist(super().items())
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

def frange(*args):
    return flist(range(*args))
def fxrange(*args):
    return fgenerator(range(*args))

