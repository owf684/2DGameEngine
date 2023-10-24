import coin

class ItemEngine:

    def __init__(self):
        self.o_coin = coin.Coin()

    def main_loop(self, objects, l_level_objects, l_game_objects, o_level_handler, o_player_engine):
        
        self.o_coin.main_loop(objects,l_level_objects, l_game_objects, o_level_handler, o_player_engine)

