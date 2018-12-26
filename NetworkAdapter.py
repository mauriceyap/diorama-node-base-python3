import constants
import socket


class NetworkAdapter:
    def __init__(self, port, nid_manager):
        self.nid_manager = nid_manager
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", port))

    def send(self, message, nid):
        self.socket.sendto(message, self.nid_manager.address_port_from_nid(nid))

    def receive(self):
        message, (address, port) = self.socket.recvfrom(constants.BUFFER_SIZE)
        return message, self.nid_manager.nid_from_address(address)
