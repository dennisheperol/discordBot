class PoopBalance:
    def __init__(self, object_info):
        self.id = object_info[0]
        self.balance = object_info[1]

    def increase_balance(self, increase):
        self.balance += increase

    def decrease_balance(self, decrease):
        self.balance -= decrease
