import xxhash
import random
import string
import time

class D_Hashmap:
    def __init__(self, depth, paddle_size, load_factor_threshold=0.7):
        self.depth = depth
        self.paddle_size = paddle_size
        self.load_factor_threshold = load_factor_threshold
        self.root_paddle = self.create_construct()
        self.collision_counts = {depth: 0 for depth in range(1, self.depth + 1)}
        self.num_items = 0

    def create_construct(self):
        root_paddle = []
        self._create_nested_list(root_paddle, self.depth)
        return root_paddle

    def _create_nested_list(self, parent_list, depth):
        if depth == 1:
            parent_list.append([])
        else:
            child_list = []
            parent_list.append(child_list)
            for _ in range(self.paddle_size):
                self._create_nested_list(child_list, depth - 1)

    def insert_item(self, key, value):
        depth_to_insert = self._hash_depth(key)
        self._insert_item_helper(self.root_paddle, key, value, depth_to_insert, self.depth)
        self.num_items += 1
        self._check_and_resize()

    def _insert_item_helper(self, parent_list, key, value, depth_to_insert, current_depth):
        if current_depth == depth_to_insert:
            if len(parent_list) < self.paddle_size:
                parent_list.append((key, value))
            else:
                # Handle collision by inserting at the depth below or above
                self.collision_counts[depth_to_insert] += 1
                self._insert_at_depth(key, value, depth_to_insert - 1)
                self._insert_at_depth(key, value, depth_to_insert + 1)
        else:
            for child_list in parent_list:
                self._insert_item_helper(child_list, key, value, depth_to_insert, current_depth - 1)

    def _insert_at_depth(self, key, value, depth):
        parent_list = self.root_paddle
        for _ in range(self.depth - depth):
            parent_list = parent_list[0]
        if len(parent_list) < self.paddle_size:
            parent_list.append((key, value))
        else:
            self.collision_counts[depth] += 1

    def _hash_depth(self, key):
        hash_value = xxhash.xxh64(key.encode()).intdigest() % (self.depth - 1)
        return hash_value + 1

    def retrieve_value(self, key):
        depth_to_retrieve = self._hash_depth(key)
        return self._retrieve_value_helper(self.root_paddle, key, depth_to_retrieve, self.depth)

    def _retrieve_value_helper(self, parent_list, key, depth_to_retrieve, current_depth):
        if current_depth == depth_to_retrieve:
            for key_value_pair in parent_list:
                if key_value_pair[0] == key:
                    return key_value_pair[1]
        else:
            for child_list in parent_list:
                result = self._retrieve_value_helper(child_list, key, depth_to_retrieve, current_depth - 1)
                if result is not None:
                    return result
        return None

    def _check_and_resize(self):
        load_factor = self.num_items / (self.paddle_size * self.depth)
        if load_factor > self.load_factor_threshold:
            self._resize()

    def _resize(self):
        new_depth = self.depth + 1
        new_paddle_size = self.paddle_size
        new_hashmap = D_Hashmap(new_depth, new_paddle_size)
        for depth in range(1, self.depth + 1):
            self._reinsert_items_at_depth(new_hashmap, depth)
        self.depth = new_depth
        self.paddle_size = new_paddle_size
        self.root_paddle = new_hashmap.root_paddle
        self.collision_counts = new_hashmap.collision_counts
        self.num_items = new_hashmap.num_items

    def _reinsert_items_at_depth(self, new_hashmap, depth):
        parent_list = self.root_paddle
        for _ in range(self.depth - depth):
            parent_list = parent_list[0]
        for key_value_pair in parent_list:
            new_hashmap.insert_item(key_value_pair[0], key_value_pair[1])
    