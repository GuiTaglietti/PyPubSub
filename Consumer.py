'''
    @authors Guilherme M. Taglietti - 192370
             José P. R. Pereira     - 192445
'''
import socket
import threading
import pickle
from Info import Info

SERVER_ADDRESS: str = "127.0.0.1"
SERVER_PORT: int = 7777

categories: dict[int, str] = {
    1: "Esportes",
    2: "Notícias de internet",
    3: "Eletrônica",
    4: "Política",
    5: "Negócios",
    6: "Viagem"
}

class Consumer:
    def __init__(self) -> None:
        self.client_id: int = 0
        self.client_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        self.lock: threading.Lock = threading.Lock()

    def new_registration(self) -> None:
        subscriptions: str = input("Insira números entre 1 e 6 para se inscrever em algum tópico: ")
        topic_numbers: list[int] = list(map(int, subscriptions.split()))
        topic_numbers.insert(0, -2)
        self.client_socket.send(pickle.dumps(topic_numbers))
        self.client_id += 1
        threading.Thread(target=self.receive_messages).start()

    def receive_messages(self) -> None:
        while True:
            msg: bytes = self.client_socket.recv(2048)
            if msg:
                info: Info = pickle.loads(msg)
                print(f"Sequência da mensagem: {info.sequence}")
                print(f"Mensagem recebida do tipo {categories[info.category]}, com valor {info.value}")

def main() -> None:
    action: str = input("Digite 'N' para registrar um novo usuário: ")
    if action.upper() == "N":
        consumer: Consumer = Consumer()
        consumer.new_registration()
    input("Pressione qualquer tecla para finalizar...")

if __name__ == "__main__":
    main()
