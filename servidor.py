import socket
import threading

def handle_client(client_socket, addr, clients):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

    client_socket.close()
    clients.remove(client_socket)

def main():
    host = '127.0.0.1'
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[*] Listening on {host}:{port}")

    clients = []

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        
        clients.append(client)

        client_handler = threading.Thread(target=handle_client, args=(client, addr, clients))
        client_handler.start()

if __name__ == "__main__":
    main()
