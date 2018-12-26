class Node:
    def __init__(self, peer_nids, my_nid, network_adapter, node_main):
        self.peer_nids = peer_nids
        self.my_nid = my_nid
        self.network_adapter = network_adapter
        self.node_main = node_main

    def run(self):
        self.node_main(self.peer_nids, self.my_nid, self.network_adapter.send, self.network_adapter.receive)

