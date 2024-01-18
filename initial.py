import grpc
import dns_pb2
import dns_pb2_grpc
import numpy as np
from utils import url_to_ip
from encryption import *
# server_port = ['50053', '50054', '50055', '50056', '50057']
server_port = ['50053', '50054', ]

def send_dns_request():
    port = np.random.choice(server_port)
    channel = grpc.insecure_channel('localhost:'+str(port))
    stub = dns_pb2_grpc.dnsServiceStub(channel)
    
    for (url, ip) in url_to_ip.items():
        request_message = dns_pb2.request(
            type="add",  
            url=url,
            ip=ip,
            timestamp='0'
        )

        # 发送请求并接收响应
        response = stub.SendMessage(request_message)
        print(response.response)


if __name__ == '__main__':
    send_dns_request()  # 调用发送 DNS 请求的客户端方法
