import coin

class _ItemEngine:

    def __init__(self):
        self.coin = coin._coin()

    def main_loop(self, objects, levelObjects, levelHandler):
        
        self.coin.main_loop(objects,levelObjects, levelHandler)

