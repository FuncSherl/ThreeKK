#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
import Persons
import Persons.base as base

class person_guanyu(base.base):
    name='base'
    describ='base class'
    
    describ_skill1=''
    describ_skill2=''
    
    blood=4
    
    
    

if __name__ == '__main__':
    print (Persons.modules_list)
    print (dir(Persons.modules_list[0]))