import hashlib

import hashlib

class D_Hashmap:
    def __init__(self, depth, paddle_size):
        self.depth = depth
        self.paddle_size = paddle_size
        self.counter = {}
        self.root_paddle = self.create_construct()


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
            for _ in range(depth):
                self._create_nested_list(child_list, depth - 1)


    def insert_item(self, item_to_insert):
        depth_to_insert = self._hash_depth(item_to_insert)
        self._insert_item_helper(self.root_paddle, item_to_insert, depth_to_insert, self.depth)


    def _insert_item_helper(self, parent_list, item_to_insert, depth_to_insert, current_depth):
        if current_depth == depth_to_insert:
            if len(parent_list) < self.paddle_size:
                parent_list.append(item_to_insert)
            else:
                # Handle collision
                raise ValueError(f"Maximum paddle size ({self.paddle_size}) reached at depth {depth_to_insert}")
        else:
            for child_list in parent_list:
                self._insert_item_helper(child_list, item_to_insert, depth_to_insert, current_depth - 1)


    def _hash_depth(self, item_to_insert):
        hash_value = hashlib.sha256(item_to_insert.encode()).hexdigest()
        depth = int(hash_value, 16) % (self.depth - 1) + 1
        return depth


    def retrieve_item(self, item_to_retrieve):
        depth_to_retrieve = self._hash_depth(item_to_retrieve)
        return self._retrieve_item_helper(self.root_paddle, item_to_retrieve, depth_to_retrieve, self.depth)


    def _retrieve_item_helper(self, parent_list, item_to_retrieve, depth_to_retrieve, current_depth):
        if current_depth == depth_to_retrieve:
            for item in parent_list:
                if item == item_to_retrieve:
                    return item
        else:
            for child_list in parent_list:
                result = self._retrieve_item_helper(child_list, item_to_retrieve, depth_to_retrieve, current_depth - 1)
                if result is not None:
                    return result
        return None
    

    