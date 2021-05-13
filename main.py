import socket
from datetime import time

import requests

open_ports = []
closed_ports = []

def scan_ports(min, max):
    for port in range(min, max + 1):
        portscan(port)


def portscan(port):
    try:
        r = requests.get(f"http://portquiz.net:{port}", timeout=10)
        if r.status_code == 200:
            # print('Port :', port, "is open.")
            open_ports.append(f"{port}, ")
            print('Port :', port, " открыт ", r.status_code)
        else:
            closed_ports.append(f"{port}, ")
        r.close()
    except:
        pass



if __name__ == '__main__':
    scan_ports(1, 65355)
    print("Открытые порты")
    print(', '.join(open_ports))
    print("Закрытые порты")
    print(', '.join(closed_ports))
    print("Сканирование завершено")
