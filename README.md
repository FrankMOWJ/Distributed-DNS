# README

This project has implemented a simple distributed DNS using Chord to organize the servers and using gRPC as the tool for communication between clients and servers. The functions implemented are as follows:

- add, update, delete, query (domain name, IP) 
-  add, delete server 
- simple implement of cache

## System Structure

In this project, there are mainly three parts:

- Central Server: maintain the global view of DNS server in  Chord
- DNS Server: response to the request from clients, when the (domain name, IP) pair is not in a server, it will transmit the request to another server based on the finger table
- Client: raise requests

<img src=".\figure\structure.png" style="zoom:80%;" />

## File Structure

- dns.proto: protocol file containing all the service of the server
- centralserver.py: class of central server
- server.py: class of DNS server
- client.py: raise requests
- utils.py: contain hash function and some (domain name, IP) pair for testing



## Test Example

We offer a test example. We let $m$ as 5, which means the Chord structure can maintain $2^5=32$ nodes at most. And some test (domain name, IP) pair are listed as follow. 

| domain name       | IP             | hash value | node |
| ----------------- | -------------- | ---------- | ---- |
| www.google.com    | 172.217.3.100  | 20         | 21   |
| www.baidu.com     | 220.181.38.148 | 24         | 31   |
| www.yahoo.com     | 98.137.11.163  | 16         | 16   |
| www.microsoft.com | 40.76.4.15     | 26         | 31   |
| www.twitter.com   | 104.244.42.65  | 30         | 31   |
| www.instagram.com | 52.200.238.83  | 10         | 12   |

The finger tables of Chord are as follow.

<img src=".\figure\chord.png" style="zoom:80%;" />

The ports are allocated as follow.

| server         | port  |
| -------------- | ----- |
| central server | 50050 |
| node 12        | 50053 |
| node 16        | 50054 |
| node 19        | 50055 |
| node 21        | 50056 |
| node 31        | 50057 |



## How to Run

- compile the protocol file

  make sure you have installed `grpcio` and `grpcio-tools` library.

```
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. dns.proto
```

- start up the central server

```shell
python centralserver.py
```

- add DNS server to Chord

  for each server, we open a new terminal, and make sure that different servers must have their unique port.

```shell
python server.py
```

- initialize DNS

```
python initial.py
```

- add, update, delete (domain name, IP)

  ​	To unify different types of requests into one interface, the project defines		

  - '0': search for IP given domain name 

  - '1': add (domain name, IP) pair
  - '2': delete (domain name, IP) pair pair
  - '3': update IP of the given domain name 

```
python client.py
```

- simulate a server quit 

  press `Ctrl+c` to shut down a server terminal.

Please give me a star ✨if you find this is beneficial to you。

​	

