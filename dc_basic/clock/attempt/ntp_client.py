import socket
import struct
import time

def get_system_time():
    # Get the current system time
    system_time = time.time()
    
    # Adjust the system time to be 5 minutes ahead
    adjusted_time = system_time + 300  # 5 minutes in seconds
    
    return adjusted_time

def ntp_client():
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Set a timeout for the socket
    client_socket.settimeout(1)
    
    # NTP server address and port (in this case, localhost)
    server_address = ('localhost', 5003)
    
    # NTP request packet (48 bytes)
    ntp_request = bytearray(48)
    ntp_request[0] = 0x1B
    
    try:
        # Send the request to the server
        client_socket.sendto(ntp_request, server_address)
        
        # Receive the response from the server
        data, address = client_socket.recvfrom(1024)
        
        if data:
            # Unpack the received data into a 64-bit unsigned integer
            ntp_time = struct.unpack('!Q', data)[0]
            
            # Convert NTP time to Unix timestamp
            unix_time = ntp_time - 2208988800
            
            # Print the received time
            print("Received time from NTP server:", time.ctime(unix_time))
            
            # Get the system time initially set to be 5 minutes ahead
            system_time = get_system_time()
            print("System time before adjustment:", time.ctime(system_time))
            
            # Synchronize the system time with the NTP time
            system_time_difference = unix_time - system_time
            synchronized_time = system_time + system_time_difference
            print("Synchronized system time:", time.ctime(synchronized_time))
            
    except socket.timeout:
        print("Request timed out")

if __name__ == "__main__":
    ntp_client()
