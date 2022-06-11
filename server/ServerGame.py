import numpy as np
from Events import *
import socket
from time import sleep
from utils.Connection import Connection
from GameStructures import *



class ServerGame:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.setblocking(False)
        self.sock.listen(10)
        self.conns = []

        self.players = {}
        self.bullets = {}

        self.W = 1000
        self.H = 500

        self.dir_vecs = {'up': np.array([0, -1], dtype=float),
                    'down': np.array([0, 1], dtype=float),
                    'left': np.array([-1, 0], dtype=float),
                    'right': np.array([1, 0], dtype=float)}

    def Run(self):
        while True:
            print('iter')
            sleep(0.050)
            self.GetNewConns()
            for conn in self.conns:
                msgs = conn.RecvMessages()
                for msg in msgs:
                    self.ProcessMessage(msg, conn)
            self.Tick()

    def Tick(self):
        for bullet in self.bullets.values():
            bullet.pos += bullet.vel

    def GetNewConns(self):
        try:
            raw_conn, addr = self.sock.accept()
            raw_conn.setblocking(False)
            self.conns.append(Connection(raw_conn))
        except Exception as e:
            print('GetNewConns: ', e)
        else:
            print(raw_conn, addr)

    def __del__(self):
        self.sock.close()

    def ProcessMessage(self, msg, author_conn):
        if type(msg) == PlayerJoinedIngoingEvent:
            self.players[msg.player_id] = Player(20, np.array([500, 500], dtype=float), msg.player_color, msg.player_id)
            player = self.players[msg.player_id]
            for conn in self.conns:
                conn.SendMessage(PlayerJoinedOutgoingEvent(player.id, player.color))
            # SEND STATE TO AUTHOR_CONN
            author_conn.SendMessage(SetInitialStateOutgoingEvent(self.players, self.bullets))
        elif type(msg) == PlayerWalkedIngoingEvent:
            player = self.players[msg.player_id]
            player.pos += self.dir_vecs[msg.dir] * player.speed
            for conn in self.conns:
                conn.SendMessage(PlayerMovedOutgoingEvent(player.pos, player.id))
        elif type(msg) == BulletShotIngoingEvent:
            player = self.players[msg.player_id]
            self.bullets[len(self.bullets)] = Bullet(player.pos.copy(), msg.vel, msg.player_id)
            for conn in self.conns:
                conn.SendMessage(BulletShotOutgoingEvent(player.pos, msg.vel, player.id))



