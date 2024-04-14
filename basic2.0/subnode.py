import Pyro4
import base64
# import sqlite3
import os


@Pyro4.expose
class SubNode:
    def __init__(self, process_id, supernode):
        self.process_id = process_id
        self.supernode = supernode
        self.coordinator_id = None
        self.current_server_index = 0

    # round robin load balancing
    def get_next_server(self):
        next_server = self.supernode.get_all_processes()[self.current_server_index]
        self.current_server_index = (
            self.current_server_index + 1
        ) % self.supernode.get_next_id()
        return next_server

    def send_message(self, destination_id, message):
        print(
            f"Node {self.process_id} sends message to node {destination_id}: {message}"
        )
        receivernode = self.supernode.get_all_processes()[destination_id]
        receivernode.receive_message(self.process_id, message)

    def receive_message(self, sender_id, message):
        if message == "Election":
            print(
                f"Node {self.process_id} receives Election message from node {sender_id}"
            )
            self.send_message(sender_id, "OK")
            self.start_election()

        elif message == "Coordinator":
            print(
                f"Node {self.process_id} receives Coordinator message from node {sender_id}"
            )
            self.coordinator_id = sender_id
            print(f"Node {self.process_id} acknowledges {sender_id} as Coordinator")

        elif message == "OK":
            print(f"Node {self.process_id} receives OK message from node {sender_id}")
            self.coordinator_id = sender_id
            print(f"Node {self.process_id} sets {sender_id} as Coordinator")

    def start_election(self):
        higher_processes = [
            pid
            for pid in self.supernode.get_all_processes().keys()
            if pid > self.process_id
        ]
        if not higher_processes:
            print(f"Node {self.process_id} is the new Coordinator")
            self.coordinator_id = self.process_id
            for pid in self.supernode.get_all_processes().keys():
                if pid != self.process_id:
                    self.send_message(pid, "Coordinator")
        else:
            max_pid = max(higher_processes)
            print(
                f"Node {self.process_id} starts Election and sends messages to higher nodes: {higher_processes}"
            )
            for pid in higher_processes:
                self.send_message(pid, "Election")

    def get_coordinator(self):
        if self.coordinator_id is None:
            self.start_election()
        return self.coordinator_id

    def upload_file(self, filename, filedata):
        if self.process_id == self.coordinator_id:
            self.get_next_server().do_upload_file(filename, filedata)   
        else:
            self.supernode.get_all_processes()[self.coordinator_id].upload_file(
                filename, filedata
            )

    def do_upload_file(self, filename, filedata):
        directory = "files"
        print(f"Node {self.process_id} uploads file {filename}")

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, filename)
        fd = base64.b64decode(filedata['data'])
        with open(file_path, "wb") as f:
            f.write(fd)


def start_server():
    # Create a Pyro daemon

    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    supernodeuri = ns.lookup("supernode")
    supernode = Pyro4.Proxy(supernodeuri)
    nodeid = supernode.get_next_id()
    # Register the PatientDBManager class with the daemon
    mysubnode = SubNode(int(nodeid), supernode)
    uri = daemon.register(mysubnode)
    ns.register("mynode" + str(nodeid), uri)
    supernode.add_subnode(uri, int(nodeid))

    # Print the uri so it can be used in the client
    print(f"Ready. The uri is: mynode{nodeid}")

    # Start the request loop
    daemon.requestLoop()


if __name__ == "__main__":
    start_server()
