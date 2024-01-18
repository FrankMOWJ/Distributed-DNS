import grpc
from concurrent import futures
import dns_pb2
import dns_pb2_grpc
import time 
import numpy as np
from utils import *
from encryption import *
'''
serviceType
'0' search for ip given url
'1' add url-ip pair
'2' delete url-ip pair
'3' update ip of the given url
'''
m = 5
port = input('port: ')
nodeid = int(input('id: '))
print('id:', nodeid)
nodeset = []
fingertable = [-1 for i in range(m)]


class DNSService(dns_pb2_grpc.dnsService):
    def __init__(self, m, id):
        self.id = id
        self.ip = dict()
        self.cache = dict()
        
    def SendMessage(self, request, context):
        serviceType = request.type
        url = request.url
        value = string_to_int_hash(url, m)
        if serviceType == 'query':
            # 查找该url是不是在该节点,如果不是通过fingertable 与其他节点建立通讯
            if url in self.ip :
                response = dns_pb2.response(response=f"Node {self.id} response: Timestamp: {request.timestamp} The ip addr of {request.url}:{self.ip[url]}")
                return response
            # 产看缓存中是否存在
            elif url in self.cache:
                response = dns_pb2.response(response=f"Node {self.id} cache response: Timestamp: {request.timestamp} The ip addr of {request.url}:{self.cache[url]}")
                return response
            # 向其他节点发送信息
            else:
                response = self.findsucc(value, request.url, serviceType='query', ip='', timestamp=str(request.timestamp))
                cnt = 0
                index = 0
                for i in range(len(response.response)):
                    if response.response[i] == ':':
                        if cnt == 2:
                            index = i
                            break
                        else:
                            cnt += 1
                self.cache[request.url] = response.response[index+1:]
                return response

        elif serviceType == 'add':
            # 先找到恰好比value大的节点ID
            nextnodeID = find(value)
            # 如果在本节点 (Y)
            if nextnodeID == self.id:
                print(f'({request.url}:,{request.ip}) is added in node {self.id}')
                self.ip[url] = request.ip
                response = dns_pb2.response(response=f"Node {self.id} response:({request.url}:,{request.ip}) has been added!")
            else:
                response = self.findsucc(value, request.url, serviceType='add', ip=request.ip, timestamp=str(request.timestamp))
            return response
            
        elif serviceType == 'delete':
            # 查找该url是不是在该节点,如果不是通过fingertable 与其他节点建立通讯
            if url in self.ip:
                response = dns_pb2.response(response=f"Node {self.id} response:({request.url},{self.ip[url]}) has been deleted!")
                del self.ip[url]
                return response
            
            else:
                response = self.findsucc(value, request.url, serviceType='delete', ip='')
                return response

        elif serviceType == 'update':
            # 查找该url是不是在该节点,如果不是通过fingertable 与其他节点建立通讯
            if url in self.ip:
                response = dns_pb2.response(response=f"Node {self.id} response:The ip of {request.url} has changed to {request.ip}!")
                self.ip[request.url] = request.ip
                return response
            else:
                response = self.findsucc(value, request.url, serviceType='update', ip=request.ip, timestamp=str(request.timestamp))
                return response
        
        server_response = dns_pb2.response(response="")
        return server_response

    def findsucc(self, key, url, serviceType, ip, timestamp='1'):
        global fingertable
        response = -1
        for i in range(m):
            if i == 0 and key < fingertable[i]:
                response = self.sendto(fingertable[i], url, serviceType, ip, timestamp)
                break
            if i == (m-1) and key >= fingertable[i]:
                response = self.sendto(fingertable[i], url, serviceType, ip, timestamp)
                break
            if key >= fingertable[i] and key < fingertable[i+1]:
                response = self.sendto(fingertable[i], url, serviceType, ip, timestamp)
                break 
        if response == -1:
            print('no response!')
        return response

    def sendto(self, nodeid, url, serviceType, ip='', timestamp='0'):
        port = -1
        for i in range(len(nodeset)):
            if nodeset[i][0] == nodeid:
                port = nodeset[i][1]
        if port == -1:
            print("port not found")
        channel = grpc.insecure_channel('localhost:'+str(port))
        stub = dns_pb2_grpc.dnsServiceStub(channel)
        
        # 构造请求消息
        request_message = dns_pb2.request(
            type=serviceType, 
            url=url,
            ip=ip,
            timestamp=str(int(timestamp)+1)
        )
        
        # 发送请求并接收响应
        response = stub.SendMessage(request_message)
        return response

    def transferValueWhenQuit(self):
        global nodeset
        nodeset = [(id, port) for (id, port) in nodeset if id != nodeid]
        nextid = find(succ=nodeid)
        # 这里还有一点不晚上，不能直接根据全局视图与最终存放节点建立通讯，而应该分局fingertable来查询
        for (url, ip) in self.ip.items():
            self.sendto(nextid, url, 'add', ip, timestamp='0')
    
    def transferValueWhenJoin(self):
        global nodeset
        # print(f'{nodeid}:', nodeset)
        for (url, ip) in self.ip.items():
            value = string_to_int_hash(url, m=5)
            node = find(value)
            # print(f'url: {url}, node:{node}')
            if node != nodeid:
                probe_response = ''
                cnt = 0
                while probe_response != 'ACK':
                    print('SYN Retry ...')
                    probe_response = connect_service.sendto(nodeid=node, flag='SYN').response
                    print(probe_response)
                    time.sleep(1)
                    if cnt >= 3:
                        break
                    cnt += 1
                    
                self.sendto(node, url, serviceType='add', ip=ip, timestamp='0')
                del self.ip[url]

dns_service = DNSService(m, nodeid)

class broadcastService(dns_pb2_grpc.broadcast):
    def SendMessage(self, request, context):
        # 在这里处理接收到的请求，并返回响应
        global nodeset
        global nodeid
        global fingertable
        # process the response
        '''
        the format of the response is as follow
        id: string ('id1, id2, ..., idn,')
        channel:  string ('channel1, channel2, ..., channeln,')
        '''
        
        node = request.id.split(',')[:-1]
        channel = request.channel.split(',')[:-1]
        if len(node) != len(channel):
            print('the length of nodeset and channelset is not matched!')
        newnodeset = []
        for (id, port) in zip(node, channel):
            newnodeset.append((int(id), port))
        newnodeset = sorted(newnodeset, key=lambda x: x[0])  # 按nodeid进行升序排序
        response = dns_pb2.response(response=f'node {str(nodeid)} receive new global view')
        nodeset = newnodeset
        buildfingertable()
        print('fingertable:', fingertable)
        # when a new server join the chord, each server check whether the (key, value) stored in them have to transfer
        # dns_service.transferValueWhenJoin()
        # print('receive broadcast:',nodeset)

        return response


    def broadcast(self, id, port, broadcast_type):
        global nodeset
        global nodeid
        # send join message to the central server
        channel = grpc.insecure_channel('localhost:50050')
        stub = dns_pb2_grpc.broadcastStub(channel)
        
        # 构造请求消息
        request_message = dns_pb2.broadcastid(
            type=str(broadcast_type),
            id=str(nodeid),
            channel=port
        )
        # 发送请求并接收响应
        response = stub.SendMessage(request_message)
        print("receive from centralServer:", response.response)

broadcast_service = broadcastService()

class connectService(dns_pb2_grpc.connect):
    async def SendMessage(self, request, context):
        if request.flag == 'SYN':
            if len(nodeset) == 0:
                response = dns_pb2.response(response="NACK")
            else:
                response = dns_pb2.response(response="ACK")
        else:
           response = dns_pb2.response(response="ACK")

        return response

    async def sendto(self, nodeid, flag):
        port = -1
        for i in range(len(nodeset)):
            if nodeset[i][0] == nodeid:
                port = nodeset[i][1]
        channel = grpc.insecure_channel('localhost:'+str(port))
        stub = dns_pb2_grpc.connectStub(channel)
        
        # 构造请求消息
        request_message = dns_pb2.probe(
           flag=flag
        )
        
        # 发送请求并接收响应
        response = stub.SendMessage(request_message)
        channel.close()
        return response

connect_service = connectService()
    
        
def find(succ):
    global nodeset
    nextnodeid = None
    print('find:',nodeset)
    for (nodeid, channel) in nodeset:
        if succ <= nodeid:
            nextnodeid = nodeid
            break
    if nextnodeid == None:
        nextnodeid = nodeset[0][0]
    return nextnodeid

def buildfingertable():
    global nodeset
    global nodeid
    for i in range(1, m+1):
        succ = (int(nodeid) + pow(2, i-1)) % (2 ** m)
        nextnodeid = find(succ=succ)
        fingertable[i-1] = nextnodeid


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    dns_pb2_grpc.add_dnsServiceServicer_to_server(dns_service, server)
    dns_pb2_grpc.add_broadcastServicer_to_server(broadcast_service, server)
    dns_pb2_grpc.add_connectServicer_to_server(connect_service, server)

    server.add_insecure_port('[::]:'+port)  
    server.start()
    print(f'DNS server {port} has set up')
    broadcast_service.broadcast(str(nodeid), port, 'join')

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        try:
            broadcast_service.broadcast(str(nodeid), port, 'quit')
            dns_service.transferValueWhenQuit()
            print(f"Server quit. Broadcasting exit message...")
        except Exception as e:
            print(f"Error during server quit: {e}")
        finally:
            server.stop(0)  # 优雅地停止 gRPC 服务器


if __name__ == '__main__':
    serve()
