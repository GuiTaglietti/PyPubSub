'''
    @authors Guilherme M. Taglietti - 192370
             José P. R. Pereira     - 192445
'''
import socket
import threading
import time
import random
import pickle
from queue import Queue
from Info import Info

UDP_SERVER_ADDRESS: str = '127.0.0.1'
UDP_SERVER_PORT: int = 5002
VALUE_MAX: int = 10
VALUE_MIN: int = 3
TIME_MAX: int = 5
TIME_MIN: int = 2
udp_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
destination: tuple[str, int] = (UDP_SERVER_ADDRESS, UDP_SERVER_PORT)

class Generator:
    def __init__(self, category: int, max_value: int, min_value: int, max_time: int, min_time: int) -> None:
        self.category: int = category
        self.max_value: int = max_value
        self.min_value: int = min_value
        self.max_time: int = max_time
        self.min_time: int = min_time
        self.queue: Queue = Queue()
        self.lock: threading.Lock = threading.Lock()

    def generate_data(self) -> None:
        while True:
            random_value: int = random.randint(self.min_value, self.max_value)
            self.queue.put(Info(sequence=0, category=self.category, value=random_value))
            time.sleep(random.randint(self.min_time, self.max_time))

    def send_data(self) -> None:
        while True:
            if not self.queue.empty():
                with self.lock:
                    info: bytes = pickle.dumps(self.queue.get())
                udp_socket.sendto(info, destination)

def main() -> None:
    num_generators: int = int(input("Insira o número de geradores que deseja: "))
    for _ in range(num_generators):
        categories: list[int] = [random.randint(0, 1) for _ in range(6)]
        for index, active in enumerate(categories):
            if active:
                generator: Generator = Generator(index + 1, VALUE_MAX, VALUE_MIN, TIME_MAX, TIME_MIN)
                threading.Thread(target=generator.generate_data).start()
                threading.Thread(target=generator.send_data).start()
    input("Pressione qualquer tecla para finalizar...")

if __name__ == "__main__":
    main()
