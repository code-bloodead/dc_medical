import socket
import time

# Function to calculate clock drift
def calculate_drift(client_time, server_time):
    return server_time - client_time

# Function to synchronize clocks using Berkeley algorithm
def synchronize_clocks(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                if not data:
                    break
                server_time = float(data.decode())
                client_time = time.time()
                drift = calculate_drift(client_time, server_time)
                conn.sendall(str(drift).encode())

# Function to send time request and receive corrected time
def request_time(server_address, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_address, port))
        current_time = time.time()
        s.sendall(str(current_time).encode())
        data = s.recv(1024)
        drift = float(data.decode())
        corrected_time = current_time + (drift / 2)
        print("Corrected time on port", port, ":", corrected_time)

def main():
    # Example ports for nodes
    ports = [5000, 5001, 5002]

    # Synchronize clocks on all ports
    for port in ports:
        synchronize_clocks(port)

    time.sleep(2)  # Wait for servers to start

    # Request and print corrected time for each port
    for port in ports:
        request_time('localhost', port)

if __name__ == "__main__":
    main()
