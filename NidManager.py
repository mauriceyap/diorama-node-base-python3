class NidManager:
    def __init__(self, nid_mappings):
        self.nid_to_address_port = {entry['nid']: (entry['ip_address'], entry['port'])
                                    for entry
                                    in nid_mappings}
        self.address_to_nid = {entry['ip_address']: entry['nid']
                               for entry
                               in nid_mappings}

    def address_port_from_nid(self, nid):
        return self.nid_to_address_port[nid] if nid in self.nid_to_address_port else None

    def nid_from_address(self, address):
        return self.address_to_nid[address] if address in self.address_to_nid else None
