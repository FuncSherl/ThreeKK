'''
Created on 2020年2月13日

@author: sherl
'''
import json
#0   1    2    3    4      5      6     7      8      9    10
#心跳、出牌、判定牌、发牌、回合开始、回合结束、游戏开始、游戏结束、发动技能、发动装备、通知、
#  11         12
#选择人物、回合开始前的初始化信息
msg_types=['heartbeat', 'playcard', 'judgement', 'getcard', 'roundstart', 'roundend', 'gamestart', 'gameend', 'skillstart', 'equipstart', 'inform',
            'pickhero', 'gameinited']



def form_msg(msg_name, myid=None, myhero=None, mycards=None, start=None, end=None, herofrom=None, heroto=None, third=None, forth=None, fifth=None, reply=True):
    kep={'msg_name':msg_name,
         'myid':myid,
         'myhero':myhero,
         'mycards':mycards,
         'start':start,
         'end':end,
         'herofrom':herofrom,
         'heroto':heroto,
         'third':third,
         'forth':forth,
         'fifth':fifth,
         'reply':reply
        }
    return json.dumps(kep)

def form_inform(msg, reply=False):
    return form_msg(msg_types[10], third=msg, reply=reply)

def form_heartbeat(reply=True):
    return form_msg(msg_types[0], reply=reply)

def form_gamestart(iden, reply=False):
    return form_msg(msg_types[6], myid=iden, reply=reply)

def form_gameend(myid, reply=False):
    return form_msg(msg_types[7], reply=reply)

def form_pickhero(myid, hero_ids, reply=True):
    return form_msg(msg_types[11], myid=myid, myhero=hero_ids, reply=reply)

def form_getcard(myid, myheroid,mycards, end, start, cards, reply=False):
    #消息发到的人物id，消息发到的英雄， 摸牌前的手牌，谁摸牌，摸得什么牌，需要回复?
    return form_msg(msg_types[3], myid=myid, myhero=myheroid, mycards=mycards,start=start,  end=end, third=cards, reply=reply)

def form_roundstart(myid, myheroid, mycards, whosround ,reply=False):
    return form_msg(msg_types[4], myid=myid, myhero=myheroid,mycards=mycards, third=whosround, reply=reply)

def form_gameinited(myid, myheroid, mycards ,herolist, reply=False):#游戏初始化完成的人物和牌信息声明 
    return form_msg(msg_types[12], myid=myid, myhero=myheroid, mycards=mycards, third=herolist, reply=reply)





if __name__ == '__main__':
    tep=form_msg('test')
    print(tep)
    print (type(json.loads(tep)))
    
    
    
    
    
    
    
    
    
    
    
    
    
    