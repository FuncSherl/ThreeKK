#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message



class base:
    cards_num_color=[0,0,0,0] #黑桃、梅花、红心、方片
    name='base'
    type=Config.Card_type_enum[0] #默认是基本牌['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
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
        return cls.active
    
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
        #返回是否命中
        #if not cls.against_names: return False  #这里通过against——names判断是否需要反馈，比如闪就不需要反馈
        #一个人对另一个人出了该牌，由该牌选择如何应对，注意这里的person都是实例
        if not cls.against_names: return True #cls.on_hit_player(cls,  person_start, person_end, card)
        
        tep=cls.on_ask_response(person_start, person_end, cards_sel=cls.against_names)
        if not tep: return True #cls.on_hit_player(person_start, person_end, card)
        return False
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        return True
        
    @classmethod
    def on_ask_response(cls, person_start, person_end ,selectcnt=1, active=False, go_on=False, cards_sel=against_names):
        #一个人对另一个人出了该牌，由该牌选择如何应对，注意这里的person都是实例
        cards_to_play=[]
        for i in person_end.cards:
            if Cards.class_list[ i[0] ].name in cards_sel:
                cards_to_play.append(i)
        #能出的牌都已经准备好了
        #playcard(self, cardtoselect, selectcnt=1, inform='出牌阶段', end=None, endnum=0, active=True):
        tep= person_end.playcard(cards_to_play, selectcnt=selectcnt, inform='%s对您使用了%s，请使用 %s'%(person_start.name, cls.name, '或'.join(cls.against_names)),\
                             end=[], endnum=0, active=active, go_on=go_on)
        return tep
        
    
    #以下函数正常情况下应该ret True，否则出牌阶段无法向下进行 
    ###############################################   shield speical
    @classmethod
    def on_attacked(cls, endperson, startperson,card):
        #return 挡不住？  startperson attack -> endperson
        #这里必须先对牌的种类进行判断,来的不一定是 attack牌
        return True
        
    @classmethod
    def on_damaged(cls, endperson, startperson, damage, card=None):
        #return过了后的伤害值,  受伤
        return damage


    ###################################################   armer special
    @classmethod
    def init_playcard(self, startperson, card=None):
        #每次准备出牌前的装备判定
        return True
    
    @classmethod
    def before_playcard(self, startperson,endperson, card=None):
        #询问出牌前的装备判定
        return True

    @classmethod
    def before_dodamage(self, startperson, endperson, damage, card=None):
        #return damage,造成伤害
        
        return damage








if __name__ == '__main__':
    tep=base()
    
    
    
    
    
    
    
    
    
    
    