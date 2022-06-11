from utils.Message import Message


class Connection:
    def __init__(self, raw_conn):
        self.raw_conn = raw_conn
        self.in_buffer = bytes(0)

    def SendMessage(self, message):
        bytes = Message(message).Serialize()
        cnt_sent = 0

        print(self.raw_conn, bytes)

        while cnt_sent < len(bytes):
            cnt_sent += self.raw_conn.send(bytes)

        return True

    def __SafeReceive(self, n):
        try:
            received = self.raw_conn.recv(n)
        except Exception as e:
            return False
        else:
            return received

    def RecvMessages(self):
        recv_batch = 1024
        cnt = 0

        received = self.__SafeReceive(recv_batch)

        while received:
            cnt += len(received)
            self.in_buffer += received
            received = self.__SafeReceive(recv_batch)

        ret, self.in_buffer = Message.ParseMessages(self.in_buffer)

        return ret

    def __del__(self):
        self.raw_conn.close()
