import requests
import time
from datetime import datetime

def synchronize_clocks(server_time_url):
    # Get the current client time in milliseconds since the Unix epoch
    client_time_request_sent = time.time() * 1000
    
    # Send a request to the server to get the server time
    response = requests.get(server_time_url)
    if response.status_code == 200:
        server_time = response.json()['serverTime']
    else:
        print(f"Error fetching server time: {response.status_code}")
        return

    # Get the client time when the response was received
    client_time_response_received = time.time() * 1000
    
    # Calculate the round-trip time and adjust the server time to estimate when the response was received
    round_trip_time = client_time_response_received - client_time_request_sent
    estimated_server_time_when_received = server_time + round_trip_time / 2
    
    # Calculate the time difference between client and server
    time_difference = client_time_response_received - estimated_server_time_when_received
    
    # Convert server time and client time to human-readable format
    server_time_str = datetime.fromtimestamp(estimated_server_time_when_received / 1000).strftime('%Y-%m-%d %H:%M:%S')
    client_time_str = datetime.fromtimestamp(client_time_response_received / 1000).strftime('%Y-%m-%d %H:%M:%S')
    
    # Print the results
    print(f"Estimated server time when response was received: {server_time_str}")
    print(f"Client time when response was received: {client_time_str}")
    print(f"Time difference (milliseconds): {time_difference:.3f}")

if __name__ == '__main__':
    # Define the URL of the server endpoint
    server_time_url = 'http://localhost:3000/getTime'
    
    # Call the function to synchronize clocks
    synchronize_clocks(server_time_url)
