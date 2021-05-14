import requests
import threading
from datetime import datetime
start_time = datetime.now()

port_start = 1
port_finish = 60000
count_threads = 5       # Количество потоков (10 потоков ловят бан)
count_ports_scanned = 0

ports = []      # Список портов для сканирования
open_ports = []
closed_ports = []
threads = []    # Потоки

finished = False        # Завершена ли программа принудительно


def scan_ports(from_port, to_port):
    """
    Диапазон сканирования
    :param from_port: Начальный порт сканирования
    :param to_port: Конечный порт сканирования
    """

    for port in range(from_port, to_port + 1):
        ports.append(port)

    print("Будет просканировано:", len(ports), "портов")
    """ Запускаем указанное количество потоков """
    for t in range(0, count_threads):
        threads.append(threading.Thread(target=runner, daemon=False).start())

    """ Ожидаем выполнения потоков """
    for thread in threads:
        while True:
            thread.join(1)
            if not thread.is_alive():
                break




def runner():
    while len(ports) != 0 and finished == False:
        portscan(ports.pop(0))

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
    except requests.ConnectTimeout as e:
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
        # Обработать исключение Ctrl-C, чтобы не отображалось сообщение об ошибке
        finished = True
        for thread in threads:
            thread.join()
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
