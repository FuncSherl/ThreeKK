#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
import Persons
import Persons.base as base

class person_guanyu(base.base):
    def __init__(self):
        pass
    
    def On_game_init(self):
        pass
    
    def On_round_init(self):
        pass
    
    

if __name__ == '__main__':
    print (Persons.modules_list)
    print (dir(Persons.modules_list[0]))