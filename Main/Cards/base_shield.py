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
    type=Config.Card_type_enum[3] #默认是基本牌['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
    against_names=[]
    damage=0
    active=True
    scop=1  #手长 
    
    def __init__(self):
        pass
    
    
    #以下必须由子类复现，凸显子类特性 
    @classmethod
    def cal_active(cls, person, card=None):
        #该person是否能够出该类牌  person为一个实例 
        if cls.active is None:#不确定,以桃的处理为例
            if person.health<person.blood:
                return  True
            return False
        return True
    
    @classmethod
    def cal_targets(cls, startperson, card=None):
        #能指定什么目标,返回目标ids,桃需要重写
        cnt=len(startperson.room.socket_list)
        #return 1,[startperson.playerid]  #仅自己
        return 1,list( range(cnt ) ).remove(startperson.playerid)  #除了自己选一个
        return cnt,list( range(cnt ) )  #所有人 



#############################################################
    @classmethod
    def on_be_playedto(cls, person_start, person_end_list, card=None):
        if not cls.against_names: return True  #这里通过against——names判断是否需要反馈，比如闪就不需要反馈
        #一个人对另一个人出了该牌，由该牌选择如何应对，注意这里的person都是实例
        for k in person_end_list:
            cards_to_play=[]
            for i in k.cards:
                if Cards.class_list[ i[0] ].name in cls.against_names:
                    cards_to_play.append(i)
            #能出的牌都已经准备好了
            #playcard(self, cardtoselect, selectcnt=1, inform='出牌阶段', end=None, endnum=0, active=True):
            tep= k.playcard(cards_to_play, inform='%s对您使用了%s，是否使用 %s'%(person_start.name, cls.name, '或'.join(cls.against_names)),\
                             end=[], endnum=1, active=False)
            if not tep: return tep
        
        
        #决斗的话需要后面换玩家，然后接着调用
        return True
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        #默认以杀为例
        damage=cls.damage+person_start.round_additional_damage_attack+person_start.next_additional_damage_attack
        person_start.next_additional_damage_attack=0  #去掉酒这种buff
        
        return person_end.drophealth(person_start, damage)
        
        
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









if __name__ == '__main__':
    tep=base()