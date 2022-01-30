from bitarray import bitarray
from operations import permute


class KeyScheduler:
    shiftsPerRound = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    def __init__(self, key: str):
        if len(key) != 8:
            raise ValueError("expected 64-bit key, got", len(key))

        # compress the 64-bit key into 56-bit
        bitkey = bitarray(endian='big')
        bitkey.frombytes(key.encode())
        output = permute(bitkey, "PBD")
        assert len(output) == 56

        self.currentRound = 0
        self.leftKey: bitarray = output[:28]
        self.rightKey: bitkey = output[:28]

    def getkey(self):
        for i in range(self.shiftsPerRound[self.currentRound]):
            self.leftKey.append(self.leftKey[0])
            self.rightKey.append(self.rightKey[0])
            self.leftKey = self.leftKey[1:]
            self.rightKey = self.rightKey[1:]

        self.currentRound += 1
        return permute(self.leftKey+self.rightKey, "DBOX")
