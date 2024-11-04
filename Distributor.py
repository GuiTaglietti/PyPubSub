import socket
import pickle
import threading
from queue import Queue
from Info import Info

TCP_SERVER_ADDRESS: str = "127.0.0.1"
TCP_SERVER_PORT: int = 7777
udp_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(("127.0.0.1", 5002))

class Distributor:
    def __init__(self) -> None:
        self.clients: list[socket.socket] = []
        self.client_interests: list[list[socket.socket]] = [[] for _ in range(7)]
        self.sequence: int = 0
        self.lock: threading.Lock = threading.Lock()
    
    def start_tcp_server(self) -> None:
        tcp_server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind((TCP_SERVER_ADDRESS, TCP_SERVER_PORT))
        tcp_server.listen()
        while True:
            client, addr = tcp_server.accept()
            self.clients.append(client)
            threading.Thread(target=self.register_client, args=(client,)).start()

    def register_client(self, client: socket.socket) -> None:
        while True:
            msg: bytes = client.recv(2048)
            if msg:
                subscription_list: list[int] = pickle.loads(msg)
                if subscription_list[0] == -1:
                    self.remove_client(client)
                    break
                elif subscription_list[0] == -2:
                    for topic in subscription_list[1:]:
                        if 1 <= topic <= 6:
                            self.client_interests[topic].append(client)

    def udp_listener(self, queues: list[Queue]) -> None:
        while True:
            data, _ = udp_socket.recvfrom(1024)
            with self.lock:
                info: Info = pickle.loads(data)
                self.sequence += 1
                info.sequence = self.sequence
                if 1 <= info.category <= 6:
                    queues[info.category - 1].put(info)

    def distribute_messages(self, queue: Queue, topic_id: int) -> None:
        while True:
            if not queue.empty():
                with self.lock:
                    info: bytes = pickle.dumps(queue.get())
                for client in self.client_interests[topic_id]:
                    try:
                        client.send(info)
                    except:
                        self.remove_client(client)

    def remove_client(self, client: socket.socket) -> None:
        for interests in self.client_interests:
            if client in interests:
                interests.remove(client)
        if client in self.clients:
            self.clients.remove(client)
            client.close()

    def initialize_threads(self) -> None:
        threading.Thread(target=self.start_tcp_server).start()
        queues: list[Queue] = [Queue() for _ in range(6)]
        threading.Thread(target=self.udp_listener, args=(queues,)).start()
        for i in range(1, 7):
            threading.Thread(target=self.distribute_messages, args=(queues[i - 1], i)).start()

def main() -> None:
    distributor: Distributor = Distributor()
    distributor.initialize_threads()
    input("Pressione qualquer tecla para finalizar...")

if __name__ == "__main__":
    main()
