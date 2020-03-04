'''
Created on 2020年2月12日

@author: sherl
'''
import os,sys
sys.path.append(os.path.abspath('.'))

import socket
import sys,json
from Common import Config,Message
from Rooms import base as Rooms_base
import threading
import time

class Server:
    def __init__(self):
        # 创建 socket 对象
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        
        # 获取本地主机名
        self.host = '0.0.0.0'#socket.gethostname()
        print ("hostname:",self.host)
        self.port = Config.Port
        
        self.serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #加入socket配置，重用ip和端口
        
        # 绑定端口号
        self.serversocket.bind((self.host, self.port))
        
        # 设置最大连接数，超过后排队
        self.serversocket.listen(5)
        print ('Server Start!')
        
    def check_con(self, c_sock):
        '''
        :向客户端发送心跳包，等待回复，确认连接
        '''
        msg=Message.form_heartbeat(reply=True)
        if not Rooms_base.base.send_map_str(c_sock, msg): return False
        try:
            tmsg=c_sock.recv(Config.BuffSize)
            if not tmsg: return False
            
        except  socket.timeout:
            print ('detected timeout')
            return False
        except:
            print ('unexpected error')
            return False
        return True
    
    def check_list_con(self, sock_list):
        ret=[]
        for i in sock_list:
            if self.check_con(i): ret.append(i)
            else: print ('One Person Droped!')
        return ret
    
    def inform_all(self, sock_list, message):
        msg=Message.form_inform_beforegame(message, reply=False)
        for i in sock_list:
            Rooms_base.base.send_map_str(i, msg)
    
    
    def form_room(self, cnt=5, roomtype=Rooms_base.base):
        kep_client=[]

        while len(kep_client)<cnt:
            # 建立客户端连接
            clientsocket,addr = self.serversocket.accept()      
            clientsocket.settimeout(Config.Timeout)
            print("In Coming: %s" % str(addr))

            kep_client.append(clientsocket)
            
            if len(kep_client)>=cnt:
                kep_client=self.check_list_con(kep_client)
                
            self.inform_all(kep_client, "player count: %d/%d"%(len(kep_client), cnt) )
            
        return roomtype(kep_client)
            #clientsocket.send(msg.encode('utf-8'))
            #clientsocket.close()
            #exception socket.timeout
            
    def main_loop(self, cnt=5):
        while True:
            print ('Forming Rooms of %d People...'%cnt)
            teproom=self.form_room(cnt)
            sd=threading.Thread(target=teproom.start, args=())
            sd.start()
        self.cleanup()
            
            
    def cleanup(self):
        self.serversocket.close()
        
        
if __name__ == '__main__':
    cnt=input('请输入房间人数(建议设置2-6)(default:3):')
    try:
        cnt=int(cnt)
    except Exception as e:
        print ('unexpected error:',str(e),' Using Default...')
        cnt=3
    tep=Server()
    tep.main_loop(cnt)

        
        
        
        
        