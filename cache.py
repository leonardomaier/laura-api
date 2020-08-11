class Cache:

    def __init__(self, threshold):
        self.cache_items = {}
        self.threshold = threshold

    def save(self, key, item):

        print(len(self.cache_items))

        if (len(self.cache_items) + 1 >= self.threshold):

            first_elem_key = list(self.cache_items.keys())[0]

            self.cache_items.pop(first_elem_key)

        self.cache_items[key] = item

    def retrieve(self, key):

        return self.cache_items[key]

    def is_cached(self, key):

        return key in self.cache_items
