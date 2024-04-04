from serial.tools import list_ports

def scanport():
    return list_ports.comports()

