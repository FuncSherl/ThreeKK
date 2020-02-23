#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Cards


class card_tao(Cards.base_basic.base):
    cards_num_color=[0,0,7,1]  #黑桃、梅花、红心、方片
    active=None    #能主动出牌吗[true, false, none]
    name='桃'
    against_names=[]
    target_nums=1  #能指定几个目标
    damage=0
    
    #scop=10  #手长 
    
    def __init__(self):
        #super().__init__()
        pass

    @classmethod
    def cal_targets(cls, startperson, card=None):
        #能指定什么目标,返回目标ids,桃需要重写
        cnt=len(startperson.room.socket_list)
        if startperson.health<startperson.blood:  return 1,[startperson.playerid]  #仅自己
        return 0,[]
        return 1,list( range(cnt ) ).remove(startperson.playerid)  #除了自己选一个
        return cnt,list( range(cnt ) )  #所有人 s
    
    
    @classmethod
    def on_be_playedto(cls, person_start, person_end, card=None):
        #返回是否命中
        return person_end.addhealth(person_start, card=card)
         

    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        #默认以杀为例
        return True





if __name__ == '__main__':
    pass