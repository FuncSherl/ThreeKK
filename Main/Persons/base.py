#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
import socket
import sys
from Common import Config,Message

class base:
    name='base'
    describ='base class'
    
    describ_skill1=''
    describ_skill2=''
    
    blood=4
    
    def __init__(self, room, pid):
        self.room=room
        self.playerid=pid   #玩家的id，即数组中的下标 
        self.mysocket=self.room.socket_list[pid]    #记录一下本实例中的socket
        
        self.alive=True
        self.health=self.blood
        self.cards=[]
        self.round_init()
        self.function_table=Message.make_msg2fun(self)
        
        
    def round_init(self):
        self.attack_cnt=0
        self.round_status=True  #回合未结束
        
        
    def round_start(self):
        self.round_init()
        self.on_roundstart()
        
    
        
        
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
    
    def on_roundstart(self, msg=None):
        #没有技能情况下就是摸2张牌，这里room.getcard可以从玩家手中摸牌，此时start为被摸牌的玩家 ，发出后状态为等待回复
        self.room.on_getcard( Config.Cardeachround, end=self.playerid, start=None,  public=False,  reply=True)
        
    def on_roundend(self, msg=None):
        if len(self.cards)>self.health:      
            #启动弃牌
            dropcnt=len(self.cards)-self.health
                  
            
        
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













