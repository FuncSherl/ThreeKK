'''
Created on 2020年2月12日

@author: sherl
'''
import socket
import sys
from tools import Config

class Server:
    def __init__(self):
        # 创建 socket 对象
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
        # 获取本地主机名
        self.host = socket.gethostname()
        print ("hostname:",self.host)
        self.port = Config.Port
        
        self.serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #加入socket配置，重用ip和端口
        
        # 绑定端口号
        self.serversocket.bind((self.host, self.port))
        
        # 设置最大连接数，超过后排队
        self.serversocket.listen(5)
        
    def check_con(self, c_sock):
        pass
    
    
    def form_room(self, cnt=5):
        kep_client=[]
        while cnt>0:
            # 建立客户端连接
            clientsocket,addr = self.serversocket.accept()      
            clientsocket.settimeout(Config.Timeout)
            print("In Coming: %s" % str(addr))
            cnt-=1
            kep_client.append(clientsocket)
        return kep_client
            #clientsocket.send(msg.encode('utf-8'))
            #clientsocket.close()
            #exception socket.timeout
            
    def send(self, msg):
        pass
        
        
        
        
        
        
        
        
        
        