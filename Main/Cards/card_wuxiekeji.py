#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message
from Cards import base_skill


class card_wuxiekeji(base_skill.base):
    cards_num_color=[1,2,0,0] #黑桃、梅花、红心、方片
    name='无懈可击'
    name_pinyin='WuXieKeJi'
    #type=Config.Card_type_enum[1] #默认是基本牌['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
    against_names=['无懈可击']
    damage=0
    active=False
    #scop=10  #手长 
    
    def __init__(self):
        pass
    
    
    #以下必须由子类复现，凸显子类特性 
    
    @classmethod
    def cal_targets(cls, startperson, card=None):
        #能指定什么目标,返回目标ids,桃需要重写
        cnt=len(startperson.room.socket_list)
        #return 1,[startperson.playerid]  #仅自己
        #return 1,list( range(cnt ) ).remove(startperson.playerid)  #除了自己选一个
        #return cnt,list( range(cnt ) )  #所有人 
        return 1,list( range(cnt ) )  #所有人 选一个



#############################################################
    @classmethod
    def on_be_playedto(cls, person_start, person_end, card=None):
        cnt=len(person_start.room.socket_list)
        tid=(person_start.playerid+1)%cnt
        
        while tid!=person_start.playerid:
            tep=cls.on_ask_response(person_start, person_start.room.heros_instance[tid], active=False, go_on=True)
            if tep: return False
            tid=(tid+1)%cnt
        
        return cls.on_hit_player(person_start, person_end, card)
        
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        #默认以杀为例
        return True
        
        











if __name__ == '__main__':
    tep=base()