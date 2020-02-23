#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message



class base(Cards.base.base):
    cards_num_color=[0,0,0,0] #黑桃、梅花、红心、方片
    name='base_armer'
    against_names=[]
    type=Config.Card_type_enum[2] #默认是XX牌['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
    active=True
    scop=1  #武器射程
    
    def __init__(self):
        pass
    
    
    #以下必须由子类复现，凸显子类特性 
    
    
    
    @classmethod
    def cal_targets(cls, startperson):
        #能指定什么目标,返回目标ids,桃需要重写
        cnt=len(startperson.room.socket_list)
        return 1,[startperson.playerid]  #仅自己
        return 1,list( range(cnt ) ).remove(startperson.playerid)  #除了自己选一个
        return cnt,list( range(cnt ) )  #所有人 



#############################################################
    @classmethod
    def on_be_playedto(cls, person_start, person_end_list, card=None):
        if not cls.against_names: return True  #这里通过against——names判断是否需要反馈，比如闪就不需要反馈
        #一个人对另一个人出了该牌，由该牌选择如何应对，注意这里的person都是实例      
        
        #决斗的话需要后面换玩家，然后接着调用
        return True
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        person_end.armer.append(card)
        if len(person_end.armer)>person_end.room.allow_armer:
            dropcards=person_end.armer[:-person_end.room.allow_armer]
            person_end.dropcard(dropcards)
        return True
        
        
    ###################################################armer special
    def before_playcard(self, startperson, card=None):
        #询问出牌前的装备判定
        return True

    def before_hit(self, startperson, endperson, card=None):
        pass








if __name__ == '__main__':
    tep=base()