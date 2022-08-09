import unittest
import enc360

class SerialTest:

    def __init__(self) -> None:
        self.last_msg = ''
        self.in_waiting = 5

    
    def write(self, buf):
        print(buf.hex())
        return len(buf)

    def read(self, n):
        return b'\x81\x01\x12\x00\x94'
    
    def flush(self):
        pass

class TestCharger(unittest.TestCase):
    def setUp(self) -> None:
        mock = SerialTest()
        self.charger = enc360.Charger(mock)
        return super().setUp()
    
    def test_read(self):
        self.charger.read(enc360.EEPROM.CC)
    
    def test_write(self):
        self.charger.set(enc360.EEPROM.CC, 278)



if __name__ == '__main__':
    unittest.main()