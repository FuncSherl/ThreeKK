'''
Created on 2020年2月13日

@author: sherl
'''
import json
#0   1    2    3    4      5      6     7      8      9    10
#心跳、出牌、判定牌、发牌、回合开始、回合结束、游戏开始、游戏结束、发动技能、发动装备、通知(游戏开始前)、
#  11         12           13
#选择人物、回合开始前的初始化信息、回合结束弃牌
msg_types=['heartbeat', 'playcard', 'judgement', 'getcard', 'roundstart', 'roundend', 'gamestart', 'gameend', 'skillstart', 'equipstart', 'inform_beforegame',
            'pickhero', 'gameinited','roundend_dropcard']

def make_msg2fun(obj_class):
    ret={}
    for i in msg_types:
        func_name='on_'+i
        ret[i]=getattr(obj_class, func_name)
    return ret


def form_msg(msg_name, myid=None, myhero=None, mycards=None, start=None, end=None,  third=None, forth=None, fifth=None, reply=True):
    kep={'msg_name':msg_name,
         'myid':myid,
         'myhero':myhero,
         'mycards':mycards,
         'start':start,
         'end':end,
         'third':third,
         'forth':forth,
         'fifth':fifth,
         'reply':reply
        }
    return json.dumps(kep)

def form_inform_beforegame( msg,myid=None, myhero=None, mycards=None, reply=False):#游戏匹配过程中的消息提示, 点发消息，不需要end
    return form_msg(msg_types[10], myid=myid, myhero=myhero,mycards=mycards, third=msg, reply=reply)

def form_heartbeat(myid=None, myhero=None, mycards=None, reply=True):# 点发消息，不需要end
    return form_msg(msg_types[0],myid=myid, myhero=myhero,mycards=mycards, reply=reply)

def form_gamestart(myid,  reply=False):#群发消息，无目标，不要end
    return form_msg(msg_types[6], myid=myid, reply=reply)

def form_gameend(myid, reply=False):#群发消息，不要end
    return form_msg(msg_types[7], myid=myid, reply=reply)

def form_pickhero(myid, hero_ids, reply=True):#安全性考虑，逐个发送，无目标消息；虽然该动作应该为周知，但是由于每个人都有此动作，故合并
    return form_msg(msg_types[11], myid=myid, myhero=hero_ids, reply=reply)

def form_getcard(myid, myheroid,mycards, end, start, cards, reply=False):
    #摸牌应该为周知动作，因此该消息会发给每个人，因此消息中需要指定end，即摸牌的主体是谁，这样非主体收到该消息只是显示动画，主体收到该消息则显示自己摸牌动画，
    #出于安全考虑，非主体的cards里面为None，只能看出摸牌张数，不能看出摸牌内容，若为显示牌面的摸牌，则里面为摸牌内容
    #消息发到的人物id，消息发到的英雄， 摸牌前的手牌，谁摸牌，摸得什么牌，需要回复?
    return form_msg(msg_types[3], myid=myid, myhero=myheroid, mycards=mycards,start=start,  end=end, third=cards, reply=reply)

def form_roundstart(myid, myheroid, mycards, end ,reply=False):#周知动作，每个玩家都应知道谁的回合开始，end指明开始回合的主体 
    return form_msg(msg_types[4], myid=myid, myhero=myheroid,mycards=mycards, end=end, start=end, reply=reply)

def form_gameinited(myid, myheroid, mycards ,herolist, reply=False):#游戏初始化完成的人物和牌信息声明 ，同pickhero
    return form_msg(msg_types[12], myid=myid, myhero=myheroid, mycards=mycards, third=herolist, reply=reply)

def form_roundend_dropcard(myid, myheroid, mycards, end, dropcnt, reply=True):#回合结束弃牌阶段，同roundstart
    return form_msg(msg_types[13], myid=myid, myhero=myheroid, mycards=mycards, start=end ,end=end, third=dropcnt, reply=reply)




if __name__ == '__main__':
    tep=form_msg('test')
    print(tep)
    print (type(json.loads(tep)))
    
    
    
    
    
    
    
    
    
    
    
    
    
    