from threading import Timer
import random
import math
import socket

from scipy.stats import uniform, norm, gamma, expon, cauchy, beta, triang

import constants


def get_triangle_delay(params):
    loc = params['a']
    scale = params['b'] - params['a']
    shape = (params['c'] - params['a']) / scale
    return triang.rvs(shape, loc=loc, scale=scale)


delay_variables = {
    "fixed": lambda params: params['value'],
    "uniform": lambda params: uniform.rvs(loc=params['a'], scale=(params['b'] - params['a'])),
    "normal": lambda params: norm.rvs(loc=params['mean'], scale=math.sqrt(params['variance'])),
    "gamma": lambda params: gamma.rvs(params['shape'], scale=params['scale']),
    "exponential": lambda params: expon.rvs(scale=(1 / params['rate'])),
    "cauchy": lambda params: cauchy.rvs(loc=params['location'], scale=params['scale']),
    "beta": lambda params: beta.rvs(params['a'], params['b']),
    "triangle": get_triangle_delay
}


class NetworkAdapter:
    def __init__(self, port, nid_manager, send_success_rates, send_delays, peer_nids):
        self.send_delays = send_delays
        self.nid_manager = nid_manager
        self.send_success_rates = send_success_rates
        self.peer_nids = peer_nids
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", port))

    def send(self, message, nid):
        if nid not in self.peer_nids:
            print(f"I tried to send a message to {nid}, but that nid doesn't belong to a node I'm connected to")
            return

        is_failed_send = random.random() > self.send_success_rates[nid] if nid in self.send_success_rates else False
        if is_failed_send:
            return

        delay = max(0, delay_variables[self.send_delays[nid]['distribution']](self.send_delays[nid]['params']))

        def send_message():
            self.socket.sendto(message, self.nid_manager.address_port_from_nid(nid))

        Timer(delay / 1000, send_message).start()

    def receive(self):
        message, (address, port) = self.socket.recvfrom(constants.BUFFER_SIZE)
        return message, self.nid_manager.nid_from_address(address)
