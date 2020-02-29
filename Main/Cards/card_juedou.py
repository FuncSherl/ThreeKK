#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message
from Cards import base_skill


class card_juedou(base_skill.base):
    cards_num_color=[1,1,0,1] #黑桃、梅花、红心、方片
    name='决斗'
    name_pinyin='JueDou'
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
        tlist=list( range(cnt ) )
        tlist.remove(startperson.playerid)
        #return 1,[startperson.playerid]  #仅自己
        return 1,tlist  #除了自己选一个
        return cnt,list( range(cnt ) )  #所有人 



############################################################# 
    @classmethod
    def on_be_playedto(cls, person_start, person_end, card=None):
        #返回是否命中
        cnt=len(person_start.room.socket_list)
        tid=(person_start.playerid+1)%cnt
        
        while tid!=person_start.playerid:
            #on_ask_response(cls, person_start, person_end ,selectcnt=1, active=False, go_on=False, cards_sel=None, againstnames=None)
            tep=cls.on_ask_response(person_start, person_start.room.heros_instance[tid], \
                                    active=False, go_on=True, cards_sel=cls.against_names[:1])
            if tep: return False
            tid=(tid+1)%cnt
        
        return True   
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        tep=cls.on_ask_response(person_start, person_end, active=False, go_on=False,  cards_sel=cls.against_names[1:])
        if tep: return  not cls.on_hit_player(person_end, person_start, card)
        #diaoxue
        damage=cls.damage+person_start.round_additional_damage_skill+person_start.next_additional_damage_skill
        person_start.next_additional_damage_skill=0  #去掉buff
        
        return person_end.drophealth(person_start, damage, card)
        
        
        
        










