'''

fcollections.py

tossing all the neat stuff from cytoolz and itertools and more in as members of collections classes.

FList member functions always return FList if it makes sense.

FGenerator member functions always return FGnenerator if it makes sense.

Exceptions are functions which should obviously return other types, like "reduce" - 
    which may return a whole host of types.

Converting between a list and a generator is done by using .tolist or .togenerator

.tolist and .togenerator can be used to ensure that something you MEAN to be a list
or generator stays and is that way.

FList() and FGenerator() can be used to convert any normal iterable to either

There's an FDict too.

'''

import cytoolz
import itertools

## --------------------------------------------------------------------------------
## BASE CLASS
## --------------------------------------------------------------------------------

class FBase(object):
    def map(self, f):
        return self.__class__(itertools.imap(f, self))
    def reduce(self, f, initializer=None):
        return reduce(f, self, initializer) if initializer else reduce(f, self)
    @property
    def concat(self):
        return self.__class__(cytoolz.concat(self))
    def diff(self, *seqs, **kwargs):
        return self.__class__(cytoolz.diff(*((self,)+seqs), **kwargs))
    def drop(self, n):
        return self.__class__(cytoolz.drop(n, self))
    @property
    def first(self):
        return cytoolz.first(self)
    @property
    def frequencies(self):
        return FDict(cytoolz.frequencies(self))
    def groupby(self, key):
        return FDict(cytoolz.groupby(key, self)).valmap(FList)
    def interleave(self, seq, swap=False):
        args = (seq, self) if swap else (self, seq)
        return self.__class__(cytoolz.interleave(args))
    def interpose(self, el):
        return self.__class__(cytoolz.interpose(el, self))
    @property
    def is_distinct(self):
        return cytoolz.isdistinct(self)
    def join(self, rightseq, leftkey, rightkey):
        return self.__class__(cytoolz.join(leftkey, self, rightkey, rightseq))
    @property
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
    @property
    def peek(self):
        first, seq = cytoolz.peek(self)
        self = self.__class__(seq)
        return first
    def pluck(self, ind):
        if cytoolz.isiterable(ind): return self.__class__(itertools.imap(FList, cytoolz.pluck(ind, self)))
        else: return self.__class__(cytoolz.pluck(ind, self))
    def reduce_by(self, key, op):
        return FDict(cytoolz.reduceby(key, op, self)) 
    def remove(self, predicate):
        return self.__class__(cytoolz.remove(predicate, self))
    @property
    def second(self):
        return cytoolz.second(self)
    def sliding_window(self, n):
        ''' assuming should always be a generator - otherwise - going to get huge '''
        return FGenerator(self.__class__(sw) for sw in cytoolz.sliding_window(n, self))
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
        return FDict(cytoolz.countby(key, self))
    def partition_by(self, f):
        return self.__class__(self.__class__(p) for p in cytoolz.partitionby(f, self))
    def pipe(self, *fs):
        return cytoolz.functoolz.pipe(self, *fs) 
    def pipe_map(self, *fs):
        return self.__class__(cytoolz.functoolz.pipe(_, *fs) for _ in self)
    
## --------------------------------------------------------------------------------
## MAIN CLASSES
## --------------------------------------------------------------------------------

class FList(FBase, list):
    def __getslice__(self, *args):
        return FList(super(FList, self).__getslice__(*args))
    @property
    def to_generator(self):
        return FGenerator(self)
    @property
    def sorted(self):
        return self.__class__(sorted(self))
    def sort_by(self, key):
        return self.__class__(sorted(self, key=key))

class FGenerator(FBase):
    def __init__(self, _iterable):
        self._iterable = _iterable
    def __iter__(self):
        return (_ for _ in self._iterable)
    @property
    def to_list(self):
        return FList(self)
    def get(self, ind, default=None):
        return cytoolz.get(ind, self, default)
    
class FDict(dict):
    def keymap(self):
        pass
    @property
    def keys(self):
        return FList(self.viewkeys())
    @property
    def values(self):
        return FList(self.viewvalues())
    @property
    def items(self):
        return FList(self.viewitems())
    def keymap(self, f):
        return FDict(cytoolz.keymap(f, self))
    def valmap(self, f):
        return FDict(cytoolz.valmap(f, self))
    def itemmap(self, f):
        return FGenerator(cytoolz.itemmap(f, self))
    def keyfilter(self, predicate):
        return FDict(cytoolz.keyfilter(predicate, self))
    def valfilter(self, predicate):
        return FDict(cytoolz.valfilter(predicate, self))
    def itemfilter(self, predicate):
        return FDict(cytoolz.itemfilter(predicate, self))
    def merge(self, *dicts, **kwargs):
        return FDict(cytoolz.merge(*((self,)+dicts), **kwargs))

## --------------------------------------------------------------------------------
## OVERWRITING STD LIB
## --------------------------------------------------------------------------------

def frange(*args):
    return FList(old_range(*args))
def fxrange(*args):
    return FGenerator(old_xrange(*args))

# replace std collections
list = FList
dict = FDict
# replace range
old_range, range = range, frange
# replace xrange
old_xrange, xrange = xrange, fxrange
