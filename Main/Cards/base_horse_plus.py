#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message



class base(Cards.base.base):
    cards_num_color=[0,0,0,0] #黑桃、梅花、红心、方片
    name='base_horse_plus'
    name_pinyin='base_horse_plus'
    type=Config.Card_type_enum[5] #默认是基本牌['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
    against_names=[]
    damage=0
    active=True
    scop=1  #手长 
    
    def __init__(self):
        pass
    
    
    
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
        person_end.add_horse_plus(card)
        return True
        
        











if __name__ == '__main__':
    tep=base()