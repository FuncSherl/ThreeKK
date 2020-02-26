#coding:utf-8
'''
Created on 2020年2月26日

@author: sherl
'''
import os
import Cards,Persons
from Common import Config,Message
import socket
import sys,json
import numpy as np


class UI_cmd:
    def __init__(self, ipstr='127.0.0.1'):
        self.ipstr=ipstr
        self.socket=self.connect_server(self.ipstr)
        self.height=30  #cmd为30行
        self.width=120 #120列个字符
        self.pannel=[]
        for i in range(self.height):
            self.pannel.append([])
            for j in range(self.width):
                self.pannel[-1].append(' ')
        #self.pannel[:,:]=ord(' ')
        #char->ascll ord('c')
        #ascll->char chr(97)
        for i in self.add_box(self.form_other_person()  ): print (i)
        
    
    def main_loop(self):
        pass
        
    
    
    def draw_panel(self, info_list, y, x):
        #y行x列为起点
        mlen=max([len(x.encode('utf-8')) for x in info_list])
        if mlen >self.width or len(info_list)>self.height: 
            print ('ERROR: str too long')
            return False
        
        y=min(y, self.height-len(info_list))
        x=min(x, self.width-mlen)
        
        
    
    def add_box(self, info_list):
        mlen=max([len(x.encode('utf-8')) for x in info_list])+2
        for i in range(len(info_list)):
            info_list[i]='|'+info_list[i]+' '*(mlen-2-len(info_list[i].encode('utf-8')))+'|'
        
        info_list.insert(0, '-'*mlen)
        info_list.append('-'*mlen)
        return info_list
    
    def form_other_person(self, name='test', health=1, armers=[], shields=[], cards=[]):
        return ['HERO:'+name+'  ' +'*'*health, 'ARMERS:'+','.join( [Cards.class_list[x[0]].name for x in armers]),\
              'SHIELDS:'+','.join( [Cards.class_list[x[0]].name for x in shields]), 'CARDS:'+'N '*len(cards)]
        
    
    
    
    ##########################################################消息分配区
    def send_recv(self, c_sock, msg=None):
        '''
        :等待回复
        :若msg不为空则先发送msg
        '''
        if msg is not None: c_sock.send(msg)
        try:
            tmsg=c_sock.recv(Config.BuffSize)
            if not tmsg: return None
            
        except  socket.timeout:
            print ('ERROR:detected timeout')
            return None
        except Exception as e:
            print ('unexpected error:', str(e))
            return None
        return json.loads(tmsg)
    
    def listen_distribute(self, msgwant=[]):
        self.function_table=Message.make_msg2fun(self)
        msg=self.room.send_recv(self.mysocket)
        if msg:
            if msgwant and msg['msg_name'] not in msgwant: return self.listen_distribute(msgwant)
            return self.function_table[msg['msg_name']](msg)
        else:
            return None
                
    #下面为消息响应区 ，该部分的函数应该与Messge中的一致，注意这里为收到消息的响应，其驱动为收到消息
    def on_heartbeat(self, msg):
        return True        

    def on_playcard(self, msg):
        return msg
        
    
    def on_judgement(self, msg):
        return False
    
    def on_getcard(self, msg):
        return False
    
    def on_roundstart(self, msg=None):
        return False
        
    def on_roundend(self, msg=None):
        return False            
        
    def on_gamestart(self, msg):
        return False
    
    def on_gameend(self, msg):
        return False
    
    def on_skillstart(self, msg):
        return False
    
    def on_equipstart(self, msg):
        return False
    
    def on_inform_beforegame(self, msg):
        return False
    
    def on_pickhero(self, msg):
        return False
    
    def on_gameinited(self, msg):
        return False
    
    def on_roundend_dropcard(self, msg):
        dropedcards=[self.cards[x]  for x in msg['third']]
        self.cards=[self.cards[x]  for x in range(len(self.cards)) if (x not in msg['third'])]
        self.room.drop_cards(dropedcards)
        
        return True
        
    
    def on_askselect(self, msg):
        #返回的msg中third中为用户选择，forth为选择的card，
        #return False
        if not msg['third'] or not msg['third'][0]:
            return False
        return msg['forth']
    
    
    
    ####################################################网络部分
    def connect_server(self, ipstr='127.0.0.1'):
        # 创建 socket 对象
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
            s.settimeout(Config.Timeout)
            # 连接服务，指定主机和端口
            s.connect((ipstr, Config.Port))
            
            s.settimeout(None)
        except  socket.timeout:
            print ('ERROR:detected timeout server not online')
            return None
        except Exception as e:
            print ('unexpected error:',str(e))
            return None
        
        return s
    
    
    
    
if __name__=="__main__":
    ipstr=input('请输入服务器IP(default:127.0.0.1)：')
    if not ipstr: ipstr='127.0.0.1'
    tep=UI_cmd(ipstr)
    
    tep.main_loop()
    
    
    
    
    
    
    
    
    
    
        