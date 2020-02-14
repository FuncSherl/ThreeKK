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
        self.playerid=pid
        self.alive=True
        self.attack_cnt=1
        self.cards=[]
        
    def on_roundstart(self):
        self.room.on_getcard( Config.Cardeachround, end=self.playerid, start=None,  public=False,  reply=False)
        
    
    def addcard(self, cards_list):
        self.cards.extend(cards_list)
    
    

if __name__ == '__main__':
    pass