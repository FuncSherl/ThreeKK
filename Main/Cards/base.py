#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message



class base:
    cards_num_color=[0,0,0,0] #黑桃、梅花、红心、方片
    active=None    #能主动被出牌吗[true, false, none]
    name='base'
    type=Config.Card_type_enum[0] #默认是基本牌
    against_names=[]
    target_nums=1  #能指定几个目标
    damage=0
    
    scop=1  #手长 
    
    def __init__(self):
        pass
    
    @classmethod
    def cal_active(cls, person):
        #该person是否能够出该类牌  person为一个实例 
        if cls.active is None:#不确定,以桃的处理为例
            if person.health<person.blood:
                return  True
            return False
        return cls.active

    @classmethod
    def on_be_playedto(cls, person_start, person_end):
        #if not cls.against_names: return True  #这里通过against——names判断是否需要反馈，比如闪就不需要反馈
        #一个人对另一个人出了该牌，由该牌选择如何应对，注意这里的person都是实例
        cards_to_play=[]
        for i in person_end.cards:
            if Cards.class_list[ i[0] ].name in cls.against_names:
                cards_to_play.append(i)
        #能出的牌都已经准备好了
        tep= person_end.playcard(cards_to_play, inform='%s对您使用了%s，是否使用 %s'%(person_start.name, cls.name, '或'.join(cls.against_names)))
        if not tep: return tep
        
        
        #决斗的话需要后面换玩家，然后接着调用
        return True
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end):
        #默认以杀为例
        damage=cls.damage+person_start.round_additional_damage_attack+person_start.next_additional_damage_attack
        person_start.next_additional_damage_attack=0  #去掉酒这种buff
        
        return person_end.drophealth(person_start, damage)
        
        











if __name__ == '__main__':
    tep=base()