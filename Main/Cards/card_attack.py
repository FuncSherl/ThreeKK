#coding:utf-8
'''
Created on 2020年2月14日

@author: sherl
'''
import Cards.base as base


class card_attack(base.base):
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








if __name__ == '__main__':
    pass