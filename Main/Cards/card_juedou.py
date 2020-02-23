#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message



class card_juedou(Cards.base_skill.base):
    cards_num_color=[1,1,0,1] #黑桃、梅花、红心、方片
    name='决斗'
    #type=Config.Card_type_enum[1] #默认是基本牌['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
    against_names=['无懈可击', '杀']
    damage=1
    #active=True
    #scop=10  #手长 
    
    def __init__(self):
        pass
    
    

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
        #一个人对另一个人出了该牌，由该牌选择如何应对，注意这里的person都是实例
        cards_to_play=[]
        for i in person_end.cards:
            if Cards.class_list[ i[0] ].name in cls.against_names:
                cards_to_play.append(i)
        #能出的牌都已经准备好了
        #playcard(self, cardtoselect, selectcnt=1, inform='出牌阶段', end=None, endnum=0, active=True):
        tep= person_end.playcard(cards_to_play, inform='%s对您使用了%s，是否使用 %s'%(person_start.name, cls.name, '或'.join(cls.against_names)),\
                             end=[], endnum=0, active=False, go_on=False)
            
            
        if not tep: #命中
            cls.on_hit_player(person_start, person_end, card)
            return True
        
        #决斗的话需要后面换玩家，然后接着调用
        if cls.against_names[0] in [Cards.class_list[x[0]].name for x in tep]:
            return False
        
        cards_to_play=[]
        for i in person_start.cards:
            if Cards.class_list[ i[0] ].name in cls.against_names:
                cards_to_play.append(i)
        return person_start.playcard(cards_to_play, inform='%s对您使用了%s，是否使用 %s'%(person_end.name, cls.name, '或'.join(cls.against_names)),\
                             end=[], endnum=0, active=False, go_on=False)
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        #默认以杀为例
        return True
        
        











if __name__ == '__main__':
    tep=base()