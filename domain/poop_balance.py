class PoopBalance:
    def __init__(self, object_info):
        self.id = object_info[0]
        self.balance = object_info[1]

    def get_id(self):
        return self.id

    def get_balance(self):
        return self.balance

    def increase_balance(self, increase):
        self.balance = self.balance + increase

    def decrease_balance(self, decrease):
        self.balance = self.balance - decrease
