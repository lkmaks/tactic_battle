
class OutgoingEvent:
    def __init__(self):
        pass


class PlayerJoinedOutgoingEvent(OutgoingEvent):
    def __init__(self, player_id, player_color):
        super().__init__()
        self.player_color = player_color
        self.player_id = player_id


class PlayerMovedOutgoingEvent(OutgoingEvent):
    def __init__(self, to, player_id):
        super().__init__()
        self.to = to
        self.player_id = player_id


class BulletShotOutgoingEvent(OutgoingEvent):
    def __init__(self, start, vel, player_id):
        super().__init__()
        self.start = start
        self.vel = vel
        self.player_id = player_id


class SetInitialStateOutgoingEvent(OutgoingEvent):
    def __init__(self, players, bullets):
        super().__init__()
        self.players = players
        self.bullets = bullets


# ======================================================================


class IngoingEvent:
    def __init__(self, player_id):
        self.player_id = player_id


class PlayerJoinedIngoingEvent(IngoingEvent):
    def __init__(self, player_id, player_color):
        super().__init__(player_id)
        self.player_color = player_color


class PlayerWalkedIngoingEvent(IngoingEvent):
    def __init__(self, player_id, dir):
        super().__init__(player_id)
        self.dir = dir


class BulletShotIngoingEvent(IngoingEvent):
    def __init__(self, player_id, vel):
        super().__init__(player_id)
        self.vel = vel
