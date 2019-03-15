#!/usr/bin/python
import argparse
import importlib

import yaml

import constants
from NetworkAdapter import NetworkAdapter
from NidManager import NidManager
from Node import Node

parser = argparse.ArgumentParser()
parser.add_argument('peer_nids',
                    metavar='peer-nids',
                    help='comma-separated list of NIDs of all peers connected to this node')
parser.add_argument('nid',
                    metavar='nid',
                    help='NID of the node')
parser.add_argument('port',
                    type=int,
                    metavar='port',
                    help='udp port to be used by this node')
parser.add_argument('node_main_function',
                    metavar='node-main-path',
                    help="the Python path to the 'main' function for this node e.g. 'diorama_node.node_main'")

if __name__ == '__main__':
    args = parser.parse_args()
    peer_nids = args.peer_nids.split(constants.PEER_NID_SEPARATOR)
    node_main_path = args.node_main_function.rpartition(constants.PYTHON_PATH_SEPARATOR)
    print(f'{constants.USER_NODE_FILES_MODULE}.{node_main_path[0]}')
    node_main = getattr(importlib.import_module(f'{constants.USER_NODE_FILES_MODULE}.{node_main_path[0]}'),
                        node_main_path[-1])
    nid_mappings = yaml.load(open(constants.NODE_ADDRESSES_FILE_PATH, 'r'))

    nid_manager = NidManager(nid_mappings)
    network_adapter = NetworkAdapter(port=args.port, nid_manager=nid_manager)
    node = Node(peer_nids, args.nid, network_adapter, node_main)
    node.run()
