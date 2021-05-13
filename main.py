import requests

open_ports = []
closed_ports = []


def scan_ports(from_port, to_port):
    """
    Диапазон сканирования
    :param from_port: Начальный порт сканирования
    :param to_port: Конечный порт сканирования
    """
    for port in range(from_port, to_port + 1):
        portscan(port)


def portscan(port):
    """
    Сканирование указанного порта
    :param port: порт сканирования
    :return: результат сканирования порта
    """
    try:
        r = requests.get(f"http://portquiz.net:{port}", timeout=1)
        if r.status_code == 200:
            open_ports.append(f"{port}, ")
            print('Port:', port, "is open.")
        else:
            closed_ports.append(f"{port}, ")
            print('Port:', port, "is closed.")
        r.close()
    except requests.ConnectTimeout as e:
        closed_ports.append(f"{port}, ")
        print('Port:', port, "is closed.")
    except Exception as e:
        print(e.message)


if __name__ == '__main__':
    try:
        scan_ports(1000, 65355)
        print("Открытые порты")
        print(', '.join(open_ports))
        print("Закрытые порты")
        print(', '.join(closed_ports))
        print("Сканирование завершено")
    except KeyboardInterrupt:
        # Обработать исключение Ctrl-C, чтобы не отображалось сообщение об ошибке
        print("Открытые порты")
        print(', '.join(open_ports))
        print("Закрытые порты")
        print(', '.join(closed_ports))
        print('Завершение работы программы.')
        exit(0)
    finally:
        input("Press Enter to exit...")