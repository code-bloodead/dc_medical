import grpc
import fileService_pb2_grpc
import fileService_pb2
import time
import requests  # Ensure you have the requests library installed: pip install requests

# Synchronize client clock with server clock
def synchronize_client_clock(server_time_url):
    # Fetch server time
    response = requests.get(server_time_url)
    if response.status_code == 200:
        server_time = response.json()['serverTime']
        # Calculate the current client time
        client_time = time.time() * 1000  # Convert to milliseconds
        # Calculate time difference
        time_difference = server_time - client_time
        print(f"Time difference: {time_difference} ms")
        return time_difference
    else:
        print("Error fetching server time")
        return 0

# Run client function with synchronization
def run_client(server_address, server_time_url):
    with grpc.insecure_channel(server_address) as channel:
        try:
            grpc.channel_ready_future(channel).result(timeout=1)
        except grpc.FutureTimeoutError:
            print("Connection timeout. Unable to connect to port")
        else:
            print("Connected")
        stub = fileService_pb2_grpc.FileserviceStub(channel)

        # Synchronize client clock before handling user inputs
        time_difference = synchronize_client_clock(server_time_url)

        # Adjust client time as necessary before handling user inputs
        # This is just printing the time difference for demonstration purposes

        handle_user_inputs(stub)

# Define server and time endpoint
server_address = '127.0.0.1:9000'
server_time_url = 'http://localhost:3000/getTime'

if __name__ == '__main__':
    run_client(server_address, server_time_url)
