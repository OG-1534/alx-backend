#!/usr/bin/python3
"""
Create a class LFUCache that inherits from BaseCaching and is a caching system:
You must use self.cache_data - dictionary from the parent class BaseCaching
You can overload def __init__(self): but don’t forget to
call the parent init: super().__init__()
def put(self, key, item):
Must assign to the dictionary self.cache_data the item value for the key key.
If key or item is None, this method should not do anything.
If the number of items in self.cache_data is higher that BaseCaching.MAX_ITEMS:
you must discard the least frequency used item (LFU algorithm)
if you find more than 1 item to discard, you must use
the LRU algorithm to discard only the least recently used
you must print DISCARD: with the key discarded and following by a new line
def get(self, key):
Must return the value in self.cache_data linked to key.
If key is None or if the key doesn’t exist in self.cache_data, return None.
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFU caching """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.queue = []
        self.counter = {}

    def put(self, key, item):
        """ assign to dictionary item value for the key key """
        if key is None or item is None:
            return

        self.cache_data[key] = item

        item_count = self.counter.get(key, None)

        if item_count is not None:
            self.counter[key] += 1
        else:
            self.counter[key] = 1

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first = self.get_first_list(self.queue)
            if first:
                self.queue.pop(0)
                del self.cache_data[first]
                del self.counter[first]
                print("DISCARD: {}".format(first))

        if key not in self.queue:
            self.queue.insert(0, key)
        self.mv_right_list(key)

    def get(self, key):
        """ return value in dictionary linked to key """
        item = self.cache_data.get(key, None)
        if item is not None:
            self.counter[key] += 1
            self.mv_right_list(key)
        return item

    def mv_right_list(self, item):
        """ moves element to the right, taking into account LFU """
        length = len(self.queue)

        idx = self.queue.index(item)
        item_count = self.counter[item]

        for i in range(idx, length):
            if i != (length - 1):
                nxt = self.queue[i + 1]
                nxt_count = self.counter[nxt]

                if nxt_count > item_count:
                    break

        self.queue.insert(i + 1, item)
        self.queue.remove(item)

    @staticmethod
    def get_first_list(array):
        """ get first element of list or None """
        return array[0] if array else None
