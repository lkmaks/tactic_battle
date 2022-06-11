import pygame
import sys
from utils.Connection import Connection
import socket
from Events import *
from GameStructures import *
import numpy as np


class ClientGame:
    def __init__(self, host, port, player_id=1, color='#ff0000'):
        # GAME STATE
        self.players = {}
        self.bullets = {}

        # SELF INFO
        self.player_id = player_id
        self.color = color

        # PYGAME VISUALS
        pygame.init()

        self.W = 1000
        self.H = 500

        self.screen = pygame.display.set_mode((self.W, self.H))
        self.clock = pygame.time.Clock()

        # CREATE CONNECTION
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.setblocking(False)
        self.conn = Connection(self.sock)

        # CONTROLS STATE
        self.pressed_keys = set()

        # SYNC DETAILS
        self.init_done = False

    def Render(self):
        self.screen.fill('#ffffff')
        for player in self.players.values():
            pygame.draw.circle(self.screen, color=player.color, center=player.pos, radius=20)
        for bullet in self.bullets.values():
            pygame.draw.circle(self.screen, color=self.players[bullet.player_id].color, center=bullet.pos, radius=3)

    def ApplyKey(self, key):
        if key == ord('w'):
            self.conn.SendMessage(PlayerWalkedIngoingEvent(self.player_id, dir='up'))
        if key == ord('a'):
            self.conn.SendMessage(PlayerWalkedIngoingEvent(self.player_id, dir='left'))
        if key == ord('s'):
            self.conn.SendMessage(PlayerWalkedIngoingEvent(self.player_id, dir='down'))
        if key == ord('d'):
            self.conn.SendMessage(PlayerWalkedIngoingEvent(self.player_id, dir='right'))

    def HandleKeydown(self, key):
        self.pressed_keys.add(key)

    def HandleKeyup(self, key):
        self.pressed_keys.remove(key)

    def HandleButtondown(self, button, pos):
        our_pos = self.players[self.player_id].pos
        bullet_vel = (pos - our_pos) / np.linalg.norm(pos - our_pos) * 10
        self.conn.SendMessage(BulletShotIngoingEvent(self.player_id, bullet_vel))

    def ProcessMessage(self, msg):
        if not self.init_done and type(msg) != SetInitialStateOutgoingEvent:
            return
        elif type(msg) == SetInitialStateOutgoingEvent:
            self.players = msg.players
            self.bullets = msg.bullets
            self.init_done = True
        elif type(msg) == PlayerJoinedOutgoingEvent:
            self.players[msg.player_id] = Player(20, np.array([500, 500], dtype=float), msg.player_color, msg.player_id)
        elif type(msg) == PlayerMovedOutgoingEvent:
            player = self.players[msg.player_id]
            player.pos = msg.to
        elif type(msg) == BulletShotOutgoingEvent:
            self.bullets[len(self.bullets)] = Bullet(msg.start, msg.vel, msg.player_id)

    def Tick(self):
        for bullet in self.bullets.values():
            bullet.pos += bullet.vel

    def Run(self):
        self.conn.SendMessage(PlayerJoinedIngoingEvent(self.player_id, self.color))

        while True:
            self.clock.tick(50)
            print('iter')

            for key in self.pressed_keys:
                self.ApplyKey(key)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.HandleKeydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.HandleKeyup(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.HandleButtondown(event.button, event.pos)

            # read all new updates from server
            messages = self.conn.RecvMessages()
            print('Read Messages: ', messages)

            for msg in messages:
                self.ProcessMessage(msg)

            self.Tick()

            self.Render()

            pygame.display.flip()

    def __del__(self):
        self.sock.close()