#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
import socket
import sys
from Common import Config,Message

class base:
    def __init__(self, room, pid):
        self.room=room
        self.playerid=pid   #玩家的id，即数组中的下标 
        self.mysocket=self.room.socket_list[pid]    #记录一下本实例中的socket
        
        self.alive=True
        self.blood=4
        self.attack_cnt=0
        self.cards=[]
    
        
    def addcard(self, cards_list):
        self.cards.extend(cards_list)
    
    #下面为消息响应区 ，该部分的函数应该与Messge中的一致
    def on_heartbeat(self, msg):
        pass
    
    def on_playcard(self, msg):
        pass
    
    def on_judgement(self, msg):
        pass
    
    def on_getcard(self, msg):
        pass
    
    def on_roundstart(self, msg):
        self.attack_cnt=0
        self.room.on_getcard( Config.Cardeachround, end=self.playerid, start=None,  public=False,  reply=False)
        
    def on_roundend(self, msg):
        if len(self.cards)>self.blood:            
            pass
        
    def on_gamestart(self, msg):
        pass
    
    def on_gameend(self, msg):
        pass
    
    def on_skillstart(self, msg):
        pass
    
    def on_equipstart(self, msg):
        pass
    
    def on_inform_beforegame(self, msg):
        pass
    
    def on_pickhero(self, msg):
        pass
    
    def on_gameinited(self, msg):
        pass
    
    def on_roundend_dropcard(self, msg):
        pass
    

    
    

if __name__ == '__main__':
    pass