#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
import Persons,Cards
import Persons.base as base

class person_guanyu(base.base):
    name='关羽'
    describ='干干干'
    name_pinyin='GuanYu'
    
    describ_skill1='武圣：出牌阶段可以将手牌中任意红牌作为一张杀使用'
    describ_skill2=''
    describ_skill3=''
    describ_skill4=''
    
    describ_skill_list=[describ_skill1, describ_skill2, describ_skill3, describ_skill4]
    
    blood=4
    
    def __init__(self, room, pid):
        super().__init__(room, pid)
    
    #################################################################
    def playcardstart(self):
        #如果英雄一开始出牌可以选择其他，这里要修改,eg.guanyu
        keep=True
        while keep:
            #[cardid, color, num]
            red_cards=[x for x in self.cards if (x[1]>=2)]  ##黑桃、梅花、红心、方片
            endlist=list(range(len(self.room.socket_list)))
            endlist.remove(self.playerid)
            if red_cards:
                res=self.playcard(red_cards, inform='发动技能武圣(请打出一张红牌或取消)？', end=endlist , endnum=[1], \
                              active=False, go_on=False   )
                if res: #如果打出了一张红牌
                    print (res)
                    card,ed=res[0][0],res[1][0]
                    card[0]=Cards.map_name_id['杀']
                    self.play_one_card(ed, card, active=True)
                    continue
            
            #如果没有红牌或者不发动技能
            keep=self.playcard(self.activecards())#出牌超时，出牌阶段结束
            #新一轮出牌,每次循环都是代表一张牌已经处理完了，比如决斗相互出牌处理完了，这里等待出一张新牌
            #这样则必须在下次循环前将该牌的相关处理完
            
    
    

if __name__ == '__main__':
    print (Persons.modules_list)
    print (dir(Persons.modules_list[0]))