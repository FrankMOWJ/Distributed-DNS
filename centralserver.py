import grpc
from concurrent import futures
import dns_pb2
import dns_pb2_grpc
import time 
import numpy as np
'''
The function of centralServer is to maintain and broadcast the 
global view of the nodeset
'''


class centralServer(dns_pb2_grpc.broadcast):
    def __init__(self):
        self.globalview = dict()

    def SendMessage(self, request, context):
        id = request.id
        new_channel = request.channel
        request_type = request.type

        # a server join
        if request_type == 'join':
            self.globalview[id] = new_channel
            print(f'server {id} join, gloabl view:', self.globalview)
            server_response = dns_pb2.response(response=f"Welcome node {id} to join in the Chord!")
        else:
            del self.globalview[id]
            print(f'server {id} quit, gloabl view:', self.globalview)
            server_response = dns_pb2.response(response=f"Bye node {id}!")

        # send the new global view to all the node survive
        self.broadcast(request_type)
        return server_response

    def getglobalview(self):
        nodeset = ''
        channelset = ''
        for (id, channel) in self.globalview.items():
            nodeset += str(id)
            nodeset += ','
            channelset += str(channel)
            channelset += ','
        return nodeset, channelset

    def broadcast(self, request_type):
        nodeset, channelset = self.getglobalview()
        print(nodeset)
        # print(nodeset, channelset)
        # send to all the node
        for port in self.globalview.values():
            channel = 'localhost:' + str(port)
            channel = grpc.insecure_channel(channel)
            stub = dns_pb2_grpc.broadcastStub(channel)
            
            # 构造请求消息
            request_message = dns_pb2.broadcastid(
                type=request_type,
                id=nodeset,
                channel=channelset
            )
            
            # 发送请求并接收响应
            response = stub.SendMessage(request_message)
            print("DNS Server Response:", response.response)
        return response


# 在这里添加其他服务类
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dns_pb2_grpc.add_broadcastServicer_to_server(centralServer(), server)
    server.add_insecure_port('[::]:50050')  
    print('centralServer has set up')
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("central server quit. Broadcasting exit message...")


if __name__ == '__main__':
    serve()
