from serial.tools import list_ports

def scanport():
    # Agora retorna uma lista de todas as portas COM disponíveis.
    return list_ports.comports()

