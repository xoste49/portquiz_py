from datetime import datetime

import requests

start_time = datetime.now()

port_start = 1
port_finish = 60000
timeout_connect = 3     # timeout в секундах

ports = []      # Список портов для сканирования
open_ports = []
closed_ports = []


def scan_ports(from_port, to_port):
    """
    Диапазон сканирования
    :param from_port: Начальный порт сканирования
    :param to_port: Конечный порт сканирования
    """

    print("Будет просканировано:", str(to_port - from_port + 1), "портов")
    for port in range(from_port, to_port + 1):
        portscan(port)


def portscan(port: int):
    """
    Сканирование указанного порта
    :param port: порт сканирования
    :return: результат сканирования порта
    """
    try:
        r = requests.get(f"http://portquiz.net:{port}", timeout=10)
        if r.status_code == 200:
            open_ports.append(f"{port}")
            print('Port:', port, "is open.")
        else:
            closed_ports.append(f"{port}")
            print('Port:', port, "is closed.", r.status_code)
        r.close()
    except requests.ConnectTimeout:
        closed_ports.append(f"{port}")
        print('Port:', port, "is closed.")
    except requests.exceptions.ConnectionError as e:
        print(e)
    except Exception as e:
        print(e)


def print_result():
    print("Просканировано:", (len(open_ports) + len(closed_ports)), "портов")
    print("Открытые порты")
    print(', '.join(open_ports))
    print("Закрытые порты")
    print(', '.join(closed_ports))


if __name__ == '__main__':
    try:
        scan_ports(port_start, port_finish)
    except KeyboardInterrupt:
        # Обработать исключение Ctrl-C
        pass
    except Exception as e:
        print(e)
    finally:
        print_result()
        print("Сканирование завершено")
        end_time = datetime.now()
        print('Прошло: {}'.format(end_time - start_time))
        input("Press Enter to exit...")
        exit(0)
