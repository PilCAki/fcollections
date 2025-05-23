from .fcollections import flist, fdict, fgenerator, frange, fxrange, fset
from .fcollections import clist, cdict, cgenerator, crange, cxrange, cset
from typing import List, Dict, Generator, Any, Set, Tuple

__all__ = [
    # New chaincollections API
    'clist', 'cdict', 'cgenerator', 'crange', 'cxrange', 'cset',
    # Backwards compatibility
    'flist', 'fdict', 'fgenerator', 'frange', 'fxrange', 'fset'
]
