#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Cards


class card_attack(Cards.base_basic.base):
    cards_num_color=[7,14,3,6]  #黑桃、梅花、红心、方片
    active=True    #能主动出牌吗[true, false, none]
    name='杀'
    against_names=['闪']
    target_nums=1  #能指定几个目标
    damage=1
    
    scop=1  #手长 
    
    def __init__(self):
        #super().__init__()
        pass

    @classmethod
    def cal_targets(cls, startperson, card=None):
        #能指定什么目标,返回目标ids,桃需要重写
        cnt=len(startperson.room.socket_list)
        #return 1,[startperson.playerid]  #仅自己
        return 1,list( range(cnt ) ).remove(startperson.playerid)  #除了自己选一个
        return cnt,list( range(cnt ) )  #所有人 s
    
    
    @classmethod
    def on_be_playedto(cls, person_start, person_end, card=None):
        #返回是否命中
        if '青釭剑' not in [Cards.class_list[ x[0] ].name for x in person_start.armer]:
            for i in person_end.shield:
                if Cards.class_list[i[0]].on_attacked(): return False
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
        return False

    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        #默认以杀为例
        damage=cls.damage+person_start.round_additional_damage_attack+person_start.next_additional_damage_attack
        person_start.next_additional_damage_attack=0  #去掉酒这种buff
        
        return person_end.drophealth(person_start, damage, card)





if __name__ == '__main__':
    pass