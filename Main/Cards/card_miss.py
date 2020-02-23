#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Cards


class card_miss(Cards.base_basic.base):
    cards_num_color=[0,0,3,12]  #黑桃、梅花、红心、方片
    active=False    #能主动被出牌吗
    name='闪'
    against_names=[]
    target_nums=0  #能指定几个目标
    damage=0
    
    scop=0  #手长
    
    def __init__(self):
        #super().__init__()
        pass
    
    @classmethod
    def on_be_playedto(cls, person_start, person_end_list, card=None):
        return True
    
    @classmethod
    def on_hit_player(cls,  person_start, person_end, card):
        return True







if __name__ == '__main__':
    pass