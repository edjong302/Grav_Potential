class Body:
    def __init__(self, init_cond):
        self.mass = init_cond[0]
        self.positions = [init_cond[1], init_cond[2]]
        self.velocities = [init_cond[3], init_cond[4]]