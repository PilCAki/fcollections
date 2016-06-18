'''

fcollections_tests.py

'''

from fcollections import *

TESTS = []
def is_test(test):
    global TESTS
    TESTS.append(test)
    return test



@is_test
def replacing_std_lib_collection():
    assert type(list) == type(FList)
    assert type(dict) == type(FDict)
    print 'passed replacing std lib collection test'

@is_test
def random_tests():
    a = range(10)
    b = range(4,13) 
    c = list(range(_) for _ in range(5,10))
    print 'c', c 
    is_even = lambda i: 'is_even' if i%2==0 else 'is_odd'
    print a.map(lambda x:x/2)
    print a.reduce(lambda a,b:a+b)
    print a.partition(5).concat
    print a.first, a.second, a.last
    print a.diff(b)
    print a.groupby(is_even)
    print a.interleave(b)
    print a.interpose('99')
    print a.is_distinct
    print c.mapcat(lambda x:x*2) 
    print a.nth(2)
    print a.partition(3)
    print a.partition_all(3)
    print a.peek
    print c.pluck(4)
    print a.reduce_by(is_even, lambda a,b:a*b)
    print a.remove(is_even)
    print a.sliding_window(4).to_list
    print a.take(5)
    print a.tail(5)
    print a.stride_by(3)
    print a.top_k(4)
    print a.unique()
    print a.count_by()
    print a.partition_by(is_even)
    import numpy as np
    print 'pipe', a.pipe(lambda x:x*3, np.asarray, np.std)
    print 'pipe_map', a.pipe_map(lambda x:x-4, lambda x:x+4, lambda x:x*2, lambda x:x-3)

@is_test
def parens_pipe_test():
    print 'parens pipe test'
    a = range(100)
    print (a.partition(10)  # partition first
      .map(lambda l:FList(l*3)) # then do some other shit
      .reduce(lambda a,b:FList(a+b)) # that's right - comment all you want
      .reduce(lambda a,b:a+b)) # now that's a very good boy

if __name__ == "__main__":
    for test in TESTS: test()
