import GameObject


class _BlockObject(GameObject._GameObject):
    def __init__(self):
        super().__init__()

        self.question_block_object = None
        self.question_block_trigger = False
        self.push_block_trigger = False
        self.release_item_trigger = False
        self.theta = 1
        self.item = None