from client.ClientGame import ClientGame
from utils.ReadConfig import ReadHostPort


pid, color = input().split()
pid = int(pid)

if color == 'red':
    color = '#ff0000'

elif color == 'green':
    color = '#00ff00'

elif color == 'blue':
    color = '#0000ff'

host, port = ReadHostPort()

game = ClientGame(host, port, pid, color)
game.Run()
