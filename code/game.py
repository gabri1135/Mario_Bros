from level import Level


class Game:
    def __init__(self, surface) -> None:
        self.display_surface = surface
        self.coin_amount=0
        
        self.level = Level(0, self.display_surface, self.increment_coin)

    def increment_coin(self, coin_value:int)->int:
        self.coin_amount+=coin_value

    def run(self):
        self.level.run()
