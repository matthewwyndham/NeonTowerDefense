

class Resource:
    def __init__(self):
        self.value = 0

    def can_spend(self, amount):
        return self.value - amount >= 0

    def spend(self, amount):
        self.value -= amount

    def gain(self, amount):
        self.value += amount

    def get(self):
        return self.value

