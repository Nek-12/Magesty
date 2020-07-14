class AI:
    def __init__(self, owner):
        self.owner = owner

    def update(self):
        pass


class PlayerControllableAI(AI):
    def __init__(self, owner):
        super().__init__(owner)
        self.moving_u = False
        self.moving_r = False
        self.moving_d = False
        self.moving_l = False

    def update(self):
        super().update()

