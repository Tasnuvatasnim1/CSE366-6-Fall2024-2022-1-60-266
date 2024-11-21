class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def limit_position(self, position):
        if position[0] < 0:
            position[0] = self.width - 1
        elif position[0] >= self.width:
            position[0] = 0

        if position[1] < 0:
            position[1] = self.height - 1
        elif position[1] >= self.height:
            position[1] = 0

        return position 
