from server.ServerGame import ServerGame
from utils.ReadConfig import ReadHostPort

host, port = ReadHostPort()

server = ServerGame(host, port)
server.Run()
