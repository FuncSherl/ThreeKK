#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
import socket
import sys
from Common import Config,Message
import Cards

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
        self.cards_must_play=[]
        self.cards_may_play=Cards.active_cards_ids
        
    #这里体现各种技能
    def roundstart(self):
        self.round_init()
        #没有技能情况下就是摸2张牌，这里room.getcard可以从玩家手中摸牌，此时start为被摸牌的玩家 
        self.room.on_getcard( Config.Cardeachround, end=self.playerid, start=None,  public=False,  reply=False)
        
    def roundend(self):
        if len(self.cards)>self.health:      
            #启动弃牌
            dropcnt=len(self.cards)-self.health
            
            for ind,i in enumerate(self.room.socket_list):
                msg=Message.form_roundend_dropcard(ind, self.room.heros_list[ind], self.room.heros_instance[ind].cards, self.playerid, dropcnt, reply=(self.playerid==ind))
                i.send(msg)
            if not self.listen_distribute(Message.msg_types[13]):
                dropedcards=self.cards[:dropcnt]
                self.cards=self.cards[dropcnt:]
                self.room.drop_cards(dropedcards)                
        return True
        
    ##############################################################################
    
    def listen_distribute(self, msgwant=None):
        msg=self.room.send_recv(self.room.socket_list[self.mysocket])
        if msg:
            if msgwant and msgwant!=msg['msg_name']:return self.listen_distribute(msgwant)
            return self.function_table[msg['msg_name']](msg)
        else:
            return None
    
        
        
    def addcard(self, cards_list):
        self.cards.extend(cards_list)
    
    
    #下面为消息响应区 ，该部分的函数应该与Messge中的一致，注意这里为收到消息的响应，其驱动为收到消息
    def on_heartbeat(self, msg):
        return False
    
    def on_playcard(self, msg):
        #重要处理，很多情况下这里因该收到该消息,即用户打出一张牌
        cards_ind=msg['third']
        st=msg['start']
        ed=msg['end']
        for i in cards_ind:
            if i >=len(self.cards) or i<0:#下标越界
                return False
            
        
        return False
    
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
        if not msg['third'][0]:
            return msg['third'][0]
        return msg['forth']
        

    
    

if __name__ == '__main__':
    pass













