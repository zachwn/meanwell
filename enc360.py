

from enum import IntEnum

class EEPROM(IntEnum):
    CC =  0x41 
    CV = 0x42
    FV = 0x43
    TC = 0x44
    COMP = 0x45
    # read only
    STATUS = 0x46
    VOUT = 0x47
    IOUT = 0x48
    ID = 0x49
    TEMP = 0x4a

    def bytes(self)->bytes:
        return bytes([self.value])
    
    def _buffer(self)->bytes:
        address = self.value & 0x0F
        return bytes([address])


class Charger:
    def __init__(self, serial_con) -> None:
        self.port = serial_con
        self._write_address = lambda x: x & 0x0F
        self._read_address = lambda x: x & 0x0F | 0x80
        self.checksum = lambda x: sum(x).to_bytes(2, 'big') 

    def encode(self, msg: bytes)->bytes:
        checksum = sum(msg).to_bytes(2, byteorder='big')
        buf = msg + checksum
        return buf

    def read(self, address: EEPROM):
        buf = self.encode(address.bytes())
        self.port.write(buf)
        reply = self.port.read(5)
        return int.from_bytes(reply[1:3], 'big')
    
    def set(self, address: EEPROM, val: int):
        playload = val.to_bytes(2, 'big')
        buf = address._buffer() + playload
        self.port.write(self.encode(buf))

