class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.position = [140, 200]
        self.size = [30, 30]
        self.speed = 10

    def move(self, direction):        
        if direction == "up":
            self.position[1] -= self.speed
        elif direction == "down":
            self.position[1] += self.speed
        elif direction == "left":
            self.position[0] -= self.speed
        elif direction == "right":
            self.position[0] += self.speed
        
        self.speed += 5
        self.position = self.environment.limit_position(self.position)

    def status(self):        
        return self.position  
