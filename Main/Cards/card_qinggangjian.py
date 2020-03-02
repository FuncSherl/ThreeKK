#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message
from Cards import base_armer


class card_qinggangjian(base_armer.base):
    cards_num_color=[1,0,0,0] #黑桃、梅花、红心、方片
    name='青釭剑'
    name_pinyin='QingGangJian'
    against_names=[]
    #type=Config.Card_type_enum[2] #默认是XX牌['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
    active=True
    scop=2  #武器射程
    
    def __init__(self):
        pass
    
    
    #以下必须由子类复现，凸显子类特性 
    
    
    
    @classmethod
    def cal_targets(cls, startperson):
        #能指定什么目标,返回目标ids,桃需要重写
        cnt=len(startperson.room.socket_list)
        return 1,[startperson.playerid]  #仅自己
        tlist=list( range(cnt ) )
        tlist.remove(startperson.playerid)
        #return 1,[startperson.playerid]  #仅自己
        return 1,tlist  #除了自己选一个
        return cnt,list( range(cnt ) )  #所有人 



#############################################################
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        if not person_end: person_end=person_start
        
        return person_end.add_armer(card)
        
        
    ###################################################armer special
    def before_playcard(self, startperson, card=None):
        #询问出牌前的装备判定
        return True

    def before_hit(self, startperson, endperson, card=None):
        return True








