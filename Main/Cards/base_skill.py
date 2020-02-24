#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message



class base(Cards.base.base):
    cards_num_color=[0,0,0,0] #黑桃、梅花、红心、方片
    name='base_skill'
    type=Config.Card_type_enum[1] #默认是基本牌['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
    against_names=['无懈可击']
    damage=1
    active=True
    scop=10  #手长 
    
    def __init__(self):
        pass
    
    
    #以下必须由子类复现，凸显子类特性 
    
    @classmethod
    def cal_targets(cls, startperson, card=None):
        #能指定什么目标,返回目标ids,桃需要重写
        cnt=len(startperson.room.socket_list)
        #return 1,[startperson.playerid]  #仅自己
        return 1,list( range(cnt ) ).remove(startperson.playerid)  #除了自己选一个
        return cnt,list( range(cnt ) )  #所有人 



#############################################################
    @classmethod
    def on_be_playedto(cls, person_start, person_end, card=None):
        if not cls.against_names: return False  #这里通过against——names判断是否需要反馈，比如闪就不需要反馈
        #一个人对另一个人出了该牌，由该牌选择如何应对，注意这里的person都是实例
        
        #决斗的话需要后面换玩家，然后接着调用
        return False
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        #默认以杀为例
        damage=cls.damage+person_start.round_additional_damage_attack+person_start.next_additional_damage_attack
        person_start.next_additional_damage_attack=0  #去掉酒这种buff
        
        return person_end.drophealth(person_start, damage)
        
        











if __name__ == '__main__':
    tep=base()