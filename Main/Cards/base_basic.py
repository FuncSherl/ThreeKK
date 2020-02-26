#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message



class base(Cards.base.base):
    cards_num_color=[0,0,0,0] #黑桃、梅花、红心、方片
    name='base'
    type=Config.Card_type_enum[0] #默认是基本牌['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
    against_names=[]
    damage=0
    active=True
    scop=1  #手长 
    
    def __init__(self):
        pass



#############################################################
    @classmethod
    def on_be_playedto(cls, person_start, person_end, card=None):
        #if not cls.against_names: return False  #这里通过against——names判断是否需要反馈，比如闪就不需要反馈
        #一个人对另一个人出了该牌，由该牌选择如何应对，注意这里的person都是实例
        if not cls.against_names: return True #cls.on_hit_player(cls,  person_start, person_end, card)
        return False
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        return True
        
        











if __name__ == '__main__':
    tep=base()