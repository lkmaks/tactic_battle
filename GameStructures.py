class Player:
    def __init__(self, hp, pos, color, id, speed=1):
        self.hp = hp
        self.pos = pos
        self.color = color
        self.id = id
        self.speed = speed


class Bullet:
    def __init__(self, pos, vel, player_id):
        self.pos = pos
        self.vel = vel
        self.player_id = player_id
