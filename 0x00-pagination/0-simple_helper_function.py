#!/usr/bin/env python3
"""Function index_range that takes two int
args page and page_size.

Function returns a tuple of size two containing
start and end index corresponding to the range of
indexes to return in a list for those particular
pagination parameters.

Page no.s are 1-indexed, i.e. the first page is page 1.
"""


from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    start and end index corresponding to the range of indexes
    """
    # if page is 1, start at 0 and end at page_size
    # if page is 2, start at ((page-1) * page_size) and
    # end at (page_size * page)
    # if page is 3, start at ((page-1) * page_size) and
    # end at (page_size * page)
    return ((page-1) * page_size, page_size * page)
