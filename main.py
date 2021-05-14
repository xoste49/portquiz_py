import requests
from datetime import datetime
start_time = datetime.now()

port_start = 1
port_finish = 60000
timeout_connect = 3     # в секундах

ports = []      # Список портов для сканирования
open_ports = []
closed_ports = []

def scan_ports(from_port, to_port):
    """
    Диапазон сканирования
    :param from_port: Начальный порт сканирования
    :param to_port: Конечный порт сканирования
    """

    for port in range(from_port, to_port + 1):
        ports.append(port)
    print("Будет просканировано:", str(to_port - from_port + 1), "портов")
    print("Будет просканировано:", len(ports), "портов")

    for port in ports:
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


if __name__ == '__main__':
    try:
        scan_ports(port_start, port_finish)
        print("Просканировано:", (len(open_ports)+len(closed_ports)), "портов")
        print("Открытые порты")
        print(', '.join(open_ports))
        print("Закрытые порты")
        print(', '.join(closed_ports))
        print("Сканирование завершено")
    except KeyboardInterrupt:
        # Обработать исключение Ctrl-C
        print("Просканировано:", (len(open_ports) + len(closed_ports)),
              "портов")
        print("Открытые порты")
        print(', '.join(open_ports))
        print("Закрытые порты")
        print(', '.join(closed_ports))
        print('Завершение работы программы.')
    except Exception as e:
        print(e)
    finally:
        end_time = datetime.now()
        print('Прошло: {}'.format(end_time - start_time))
        input("Press Enter to exit...")
        exit(0)
