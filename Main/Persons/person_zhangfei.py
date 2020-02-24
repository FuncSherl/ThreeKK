#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
import Persons,Cards
import Persons.base as base

class person_zhangfei(base.base):
    name='张飞'
    describ='砍砍砍'
    
    describ_skill1=''
    describ_skill2=''
    describ_skill3=''
    describ_skill4=''
    
    describ_skill_list=[describ_skill1, describ_skill2, describ_skill3, describ_skill4]
    
    blood=4
    
    def activecards(self):
        #当前的牌中有哪些是可以主动出的
        ret=[]
        for i in self.cards:
            if Cards.class_list[i[0]].cal_active(self):
                #张飞可不用下面这句判断 
                #if Cards.class_list[i[0]].name=='杀' and self.attack_cnt>=self.room.allow_attack_cnt:continue
                ret.append(i)
        return ret
    
    

if __name__ == '__main__':
    print (Persons.modules_list)
    print (dir(Persons.modules_list[0]))