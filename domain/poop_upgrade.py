class PoopUpgrade:
    def __init__(self, object_info):
        self.id = object_info[0]
        self.chance = object_info[1]

    def get_id(self):
        return self.id

    def get_chance(self):
        return self.chance

    def increase_chance(self, increase=1):
        self.chance = self.chance + increase
