import serial
import serial.tools.list_ports


class Aten:
    def __init__(self, dummy=False):
        self.dummy = dummy
        if self.dummy:
            return
        port = [i for i in serial.tools.list_ports.comports() if i.description.startswith('USB-SERIAL CH340')][0].device
        self.port = serial.Serial(port, 19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                  bytesize=serial.EIGHTBITS)
        self.port.flush()

    def switch(self, inp):
        if self.dummy:
            return
        cmd = f"sw i0{inp}"
        # cmd = "read"
        self.port.write((cmd + "\n").encode("utf-8"))
        a = self.port.read_all()
        x = 0


if __name__ == '__main__':
    a = Aten()
    a.switch(3)
