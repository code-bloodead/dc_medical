# Example usage:
import Pyro4
import os


@Pyro4.expose
class SuperNode:
    processes = {}

    def get_next_id(self):
        return len(self.processes)

    def add_subnode(self, subnodeuri, subnodeid):
        print(f"Subnode {subnodeuri} added to the network")
        self.processes[subnodeid] = Pyro4.Proxy(subnodeuri)

    def start_election(self):
        self.processes[0].start_election()

    def get_all_processes(self):
        return self.processes

    def get_coordinator(self):
        return self.processes[0].get_coordinator()

    def upload_file(self, filename, filedata):
        coordinator = self.get_coordinator()
        response = self.processes[coordinator].upload_file(filename, filedata)
        return response

if __name__ == "__main__":
    daemon = Pyro4.Daemon()
    uri = daemon.register(SuperNode)
    ns = Pyro4.locateNS()
    ns.register("supernode", uri)
    print("SuperNode is ready.")
    daemon.requestLoop()
