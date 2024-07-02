class D_Hashmap():
    def __init__(self, depth, paddle_size):
        self.depth = depth
        self.paddle_size = paddle_size
        self.create_construct()

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

    