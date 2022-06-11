import pickle


def int_to_bytes(n):
    res = []
    for i in range(4):
        res.append(n % 256)
        n //= 256

    arr = bytearray(4)
    for i in range(4):
        arr[i] = res[i]

    return bytes(arr)


def bytes_to_int(arr):
    res = 0
    for i in range(3, -1, -1):
        res *= 256
        res += int(arr[i])

    return res


class Message:
    def __init__(self, dict):
        self.dict = dict
        self.msg_len = 1024

    def Serialize(self):
        msg = pickle.dumps(self.dict)
        return int_to_bytes(len(msg)) + msg

    @staticmethod
    def ParseMessages(buf):
        i = 0
        res = []
        while i + 4 <= len(buf):
            msglen = bytes_to_int(buf[i:i+4])
            if i + 4 + msglen <= len(buf):
                msg_bytes = buf[i + 4: i + 4 + msglen]
                res.append(pickle.loads(msg_bytes))
                i += 4 + msglen
            else:
                break

        return res, buf[i:]
