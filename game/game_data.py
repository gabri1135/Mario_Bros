class LevelData:
    def __init__(self) -> None:
        self.coin_amount: int = 0
        self.health: int = 4
        self.record: int = -1
        self.stars: list[bool] = [False, False, False]

    def increment_coin(self, coin_value: int):
        self.coin_amount += coin_value

    def increment_health(self, value: int = 0.5):
        self.health += int(value*4)
        if self.health > 4:
            self.health = 4

    def get_damage(self, value: int = 0.25):
        self.health -= int(value*4)

    def get_star(self, index):
        self.stars[index] = True

    def game_over(self):
        self.health = 0
