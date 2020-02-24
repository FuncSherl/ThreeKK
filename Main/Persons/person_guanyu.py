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
    
    describ_skill1=''
    describ_skill2=''
    
    blood=4
    
    
    

if __name__ == '__main__':
    print (Persons.modules_list)
    print (dir(Persons.modules_list[0]))