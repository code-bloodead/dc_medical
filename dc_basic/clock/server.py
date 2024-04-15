import socket
import time

def server():
    # Define server host and port
    host = '127.0.0.1'
    port = 12345

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server listening on port", port)

    while True:
        conn, addr = server_socket.accept()
        print("Connected by", addr)

        # Get current time
        current_time = time.time()
        conn.sendall(str(current_time).encode())

        conn.close()

if __name__ == "__main__":
    server()
