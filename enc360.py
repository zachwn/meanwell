
from enum import Enum

class Eprom(Enum):
    CC =  b'\x41' # constant current
    CV = b'\x42'
    FV = b'\x43' # float voltage
    TC = b'\x44' # taper current
    COMP = b'\x45' # (air) temp comp
    STATUS = b'\x46' # status
    VOUT = b'\x47' # voltage output
    IOUT = b'\x48' # current output
    ID = b'\x49' # device id
    TEMP = b'\x4a' # battery temp

class Enc360:
    def __init__(self, serial) -> None:
        self.serial = serial
        self.address = lambda cmd: (cmd[0] & 0x0F).to_bytes(1, byteorder='big')
        self.response = lambda cmd: (cmd[0] & 0x0F | 0x80).to_bytes(1, byteorder='big')
        self.checksum = lambda msg: sum(msg).to_bytes(2, byteorder='big')
        self.nreply = 5 # number of bytes in reply


    def encode(self, msg):
        '''Encoded msg to be transmitted with a checksum. returns bytearray'''
        if type(msg) is str:
            msg = bytearray(msg, 'uft-8')
        msg = bytearray(msg)
        msg.extend(self.checksum(msg))
        return msg
    
    def decode(self, reply:bytes, msg=None)->int:
        '''Decode a reply and return the payload. passing the 
        original msg ensures that the expected repsones is read'''
        if len(reply) != self.nreply:
            raise ValueError('Incorrect reply')
        if msg and self.response(msg[0]) != reply[0]:
            raise Exception('Responding to a different command')
        if self.checksum(reply[:-2]) != reply[-2:]:
            raise Exception('invalid checksum')
        playload = reply[1:3]
        return int.from_bytes(playload, byteorder='big')
    






