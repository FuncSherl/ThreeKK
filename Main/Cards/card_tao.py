#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
from  Cards import base_basic
import Cards

class card_tao(base_basic.base):
    cards_num_color=[0,0,7,1]  #黑桃、梅花、红心、方片
    active=None    #能主动出牌吗[true, false, none]
    name='桃'
    name_pinyin='Tao'
    describe='你在想peach'
    
    against_names=[]
    target_nums=1  #能指定几个目标
    damage=0
    
    #scop=10  #手长 
    
    def __init__(self):
        #super().__init__()
        pass

    @classmethod
    def cal_targets(cls, startperson, card=None):
        #能指定什么目标,返回目标ids,桃需要重写
        cnt=len(startperson.room.socket_list)
        rt=[x.playerid for x in startperson.room.heros_instance if x.health<=0]
        if startperson.round_status and startperson.health<startperson.blood:  rt.append(startperson.playerid)  #仅自己
        rt=list(set(rt))
        return 1,rt
        
    
    
    

    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        #默认以杀为例
        if not person_end: person_end=person_start
        return person_end.addhealth(person_start, 1, card=card)
        




if __name__ == '__main__':
    pass