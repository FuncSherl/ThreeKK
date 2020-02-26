#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
import Persons,Cards
from Common import Config,Message
import Persons.base as base

class person_zhouyu(base.base):
    name='周瑜'
    describ='摸摸摸'
    
    describ_skill1=''
    describ_skill2=''
    describ_skill3=''
    describ_skill4=''
    
    describ_skill_list=[describ_skill1, describ_skill2, describ_skill3, describ_skill4]
    
    blood=4
    
    
    def __init__(self, room, pid):
        super().__init__(room, pid)
    
    #这里体现各种技能
    def roundstart(self):
        self.round_init()
        #没有技能情况下就是摸2张牌，这里room.getcard可以从玩家手中摸牌，此时start为被摸牌的玩家 
        self.room.on_getcard( Config.Cardeachround+1, end=self.playerid, start=None,  public=False,  reply=False)
    

