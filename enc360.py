
from base64 import encode
from enum import Enum
from msilib.schema import Error
from time import sleep

class Eprom(Enum):
    CC =  b'\x41' # constant current (stage 1)
    CV = b'\x42'  # constant voltage (stage 2)
    FV = b'\x43' # float voltage    (stage 3)
    TC = b'\x44' # taper current    (stage 3)
    COMP = b'\x45' # (air) temp comp
    # read only
    STATUS = b'\x46' # status
    VOUT = b'\x47' # voltage output
    IOUT = b'\x48' # current output
    ID = b'\x49' # device id
    TEMP = b'\x4a' # battery temp

class Enc360:
    def __init__(self, serial_con) -> None:
        self.port = serial_con
        self.address = lambda cmd: (cmd[0] & 0x0F).to_bytes(1, byteorder='big')
        self.response = lambda cmd: (cmd[0] & 0x0F | 0x80).to_bytes(1, byteorder='big')
        self.checksum = lambda msg: sum(msg).to_bytes(2, byteorder='big')
        self.nreply = 5 # number of bytes in reply
        self.delay = 0.03 # delay in secs

    def encode(self, msg):
        '''Encoded msg to be transmitted with a checksum. returns bytearray'''
        if type(msg) is str:
            msg = bytearray(msg, 'uft-8')
        buf = bytearray(msg)
        buf.extend(self.checksum(msg))
        return buf
    
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

    def _tx(self, buf):
        n = self.port.write(buf)
        if not n:
            raise TimeoutError('Serial connect timed out, failed to write ' + buf.hex())
        if n != len(buf):
            raise IOError('Incorrect number of bytes writen, wrote {} bytes. Tried to write: {}'.format(n, buf))
        self.port.flush()

    def read(self, cmd: bytes)->int:
        buf = self.encode(cmd)
        self._tx(buf)
        if self.port.in_waiting < 5:
            sleep(self.delay)
        reply = self.port.read(5)
        return self.decode(reply, buf)
    
    def write(self, cmd: bytes, value: int):
        playload = value.to_bytes(2, byteorder='big')
        msg = cmd + playload
        buf = self.encode(msg)
        self._tx()
        r = self.read(cmd)
        if r != value:
            raise ValueError('Failed to change value')
        return r

    
    


        


