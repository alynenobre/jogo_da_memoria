import socket
import threading
import pickle

def handle_client(client_socket, addr, clientes):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            data = pickle.loads(data)

        client_socket.close()
        # Remova o cliente da lista de clientes ao desconectar
        print(f"[*] {clientes[client_socket]} disconnected")
        del clientes[client_socket]
        # Envie a lista atualizada de clientes para todos os clientes
        enviar_lista_clientes(clientes)
    except (ConnectionResetError, EOFError) as e:
        # Lida com erros de desconexão abrupta
        print(f"[*] {clientes[client_socket]} disconnected abruptly: {e}")
        client_socket.close()
        del clientes[client_socket]
        enviar_lista_clientes(clientes)


def enviar_lista_clientes(clientes):
    lista_nomes = list(clientes.values())
    data = pickle.dumps(lista_nomes)
    for cliente in clientes:
        cliente.send(data)


def main():
    host = '172.16.10.194'
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[*] Listening on {host}:{port}")

    clientes = {}  # Dicionário para armazenar clientes conectados

    while True:
        client, addr = server.accept()
        # Receba os dados serializados do cliente
        serialized_data = client.recv(1024)
        nome = pickle.loads(serialized_data)

        # Adicione o cliente à lista de clientes
        clientes[client] = nome
        # Envie os dados recebidos para todos os outros clientes
        serialized_data = client.recv(1024)
        data = pickle.loads(serialized_data)
        if data == "LISTA_CLIENTES":
            enviar_lista_clientes(clientes)

        # Printe a lista atualizada de clientes na main
        print("[*] Lista de clientes conectados:", clientes.values())
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Inicie uma thread para lidar com o cliente
        client_handler = threading.Thread(target=handle_client, args=(client, addr, clientes))
        client_handler.start()

        # Imprima a lista de clientes da main
        print("[*] Lista de clientes conectados:", clientes.values())
        # Envie a lista atualizada de clientes para todos os clientes

        

if __name__ == "__main__":
    main()
