#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message



class base(Cards.base.base):
    cards_num_color=[0,0,0,0] #黑桃、梅花、红心、方片
    name='base_shield'
    name_pinyin='base_shield'
    type=Config.Card_type_enum[3] #默认是基本牌['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
    against_names=[]
    damage=0
    active=True
    scop=1  #手长 
    
    def __init__(self):
        pass
    
    
    #以下必须由子类复现，凸显子类特性 
    
    @classmethod
    def cal_targets(cls, startperson, card=None):
        #能指定什么目标,返回目标ids,桃需要重写
        cnt=len(startperson.room.socket_list)
        return 1,[startperson.playerid]  #仅自己
        return 1,list( range(cnt ) ).remove(startperson.playerid)  #除了自己选一个
        return cnt,list( range(cnt ) )  #所有人 



#############################################################    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        person_end.add_shield(card)
        return True
        
        
    ###############################################shield speical
    @classmethod
    def on_attacked(cls, card):
        #return 能否挡住
        if Cards.class_list[card[0]].name=='杀':
            if card[1]==0 or card[1]==1: return True
        return False
        
    @classmethod
    def on_damaged(cls, damage):
        #return过了后的伤害值
        return damage



    ###################################################armer special
    @classmethod
    def before_playcard(self, startperson, card=None):
        #询问出牌前的装备判定
        return True

    @classmethod
    def before_hit(self, startperson, endperson, card=None):
        return True






if __name__ == '__main__':
    tep=base()