def ReadHostPort():
    file = open('config.txt', 'r')
    ip, port = file.read().split()[:2]
    port = int(port)
    return ip, port
