import json
from typing import Self


class CurrentLevelData:
    def __init__(self, id, coin_amount, health, stars) -> None:
        self.level_id = id
        self.coin_amount: int = coin_amount
        self.health: int = health
        #self.record: int = -1
        self.stars: list[bool] = stars

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


class Level:
    def __init__(self, stars=[False, False, False]) -> None:
        self.stars: list[bool] = stars
        #record: int = -1


class UserData:
    def __init__(self, coin_amount: int, health: int, max_level: int, levels: list[Level]) -> None:
        self.coin_amount: int = coin_amount
        self.health: int = health
        self.max_level: int = max_level
        self.levels: list[Level] = levels
        assert len(self.levels) == self.max_level+1, 'Error number levels'

    @staticmethod
    def reset():
        return UserData(0, 8, 0, [Level()])

    @staticmethod
    def read() -> Self:
        try:
            with open('userData.json', 'r') as fileData:
                data = json.loads(fileData.read())
                levels = [Level(stars=l['stars']) for l in data['levels']]
                return UserData(data['coin_amount'], data['health'], data['max_level'], levels)
        except FileNotFoundError:
            return UserData(0, 8, 0, [Level()])

    def get_life(self) -> int:
        return r if (r := self.health % 4) != 0 else 4

    def start_level(self, level_id) -> CurrentLevelData:
        life = self.get_life()
        return CurrentLevelData(level_id, self.coin_amount, life, self.levels[level_id].stars.copy())

    def new_max_level(self, new_max_level):
        for _ in range(new_max_level-self.max_level):
            self.levels.append(Level())
        self.max_level = new_max_level

    def save_progress(self, new_data: CurrentLevelData):
        self.health -= self.get_life()
        if new_data.health > 0:
            self.coin_amount = new_data.coin_amount
            self.health += new_data.health
            self.levels[new_data.level_id].stars = new_data.stars
        self.save()

    def save(self):
        levels = [{'stars': level.stars} for level in self.levels]
        data = {
            'coin_amount': self.coin_amount,
            'health': self.health,
            'max_level': self.max_level,
            'levels': levels}
        with open('userData.json', 'w') as fileData:
            fileData.write(json.dumps(data))
