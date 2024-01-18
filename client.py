import grpc
import dns_pb2
import dns_pb2_grpc
import numpy as np
from utils import url_to_ip
from encryption import *
server_port = ['50053', '50054', '50055', '50056', '50057']

#  serviceType
# '0' search for ip given url
# '1' add url-ip pair
# '2' delete url-ip pair
# '3' update ip of the given url

def transform(request_type):
    mapping = {
        '0': 'query',
        '1': 'add',
        '2': 'delete',
        '3': 'update'
    }
    return mapping[request_type]

def send_dns_request():
    # randomly connnect to a server
    port = np.random.choice(server_port)
    channel = grpc.insecure_channel('localhost:'+str(port))
    stub = dns_pb2_grpc.dnsServiceStub(channel)

    while True:
        request_type = input('request type(0: query, 1: add, 2:delete, 3:update):')
        url = input('input domain name: ')
        ip = ''
        if request_type == '1' or request_type == '3':
            ip = input('input the corresponding IP:')

        # request message
        request_message = dns_pb2.request(
            type=request_type,  
            url=url,
            ip=ip,
            timestamp='0'
        )

        response = stub.SendMessage(request_message)
        print(response.response)


if __name__ == '__main__':
    send_dns_request() 
