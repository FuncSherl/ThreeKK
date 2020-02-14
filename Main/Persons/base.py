#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
import socket
import sys

class base:
    def __init__(self, room):
        self.room=room
        self.alive=True
        self.attack_cnt=1
        self.cards=[]
        
    
    
    def getcard(self, cards_list):
        self.cards.extend(cards_list)
    
    

if __name__ == '__main__':
    pass