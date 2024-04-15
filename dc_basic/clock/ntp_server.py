import socket
import time

def ntp_server():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the localhost and port 123 (standard NTP port)
    server_socket.bind(('localhost', 5003))
    
    while True:
        # Receive data from the client and the client's address
        data, address = server_socket.recvfrom(1024)
        
        if data:
            # Get current time in seconds since epoch
            current_time = time.time()
            
            # Convert the time to NTP format (number of seconds since Jan 1, 1900)
            ntp_time = current_time + 2208988800
            
            # Pack the time into a 64-bit binary format
            ntp_data = int(ntp_time).to_bytes(8, byteorder='big')
            
            # Send the NTP time back to the client
            server_socket.sendto(ntp_data, address)

if __name__ == "__main__":
    ntp_server()
