import socket
import time

def client():
    # Define server host and port
    host = '127.0.0.1'
    port = 12345

    # Number of iterations
    iterations = 5

    for i in range(iterations):
        # Create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Receive server time
        server_time_str = client_socket.recv(1024).decode()
        server_time = float(server_time_str)

        # Calculate round trip time
        round_trip_time = time.time() - server_time

        # Calculate offset
        offset = round_trip_time / 2

        # Calculate synchronized time
        synchronized_time = time.time() + offset

        print("Iteration", i+1)
        print("Server time:", server_time)
        print("Round trip time:", round_trip_time)
        print("Offset:", offset)
        print("Synchronized time:", synchronized_time)

        client_socket.close()

        # Sleep for a while before the next iteration
        time.sleep(1)

if __name__ == "__main__":
    client()
