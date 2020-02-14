'''
Created on 2020年2月13日

@author: sherl
'''
import json
#0   1    2    3    4      5      6     7      8      9    10
#心跳、出牌、判定牌、发牌、回合开始、回合结束、游戏开始、游戏结束、发动技能、发动装备、通知、
#  11
#选择人物
msg_types=['heartbeat', 'playcard', 'judgement', 'getcard', 'roundstart', 'roundend', 'gamestart', 'gameend', 'skillstart', 'equipstart', 'inform',
            'pickhero']



def form_msg(msg_name, myid=None, myhero=None, start=None, end=None, herofrom=None, heroto=None, third=None, forth=None, fifth=None, reply=True):
    kep={'msg_name':msg_name,
         'myid':myid,
         'myhero':myhero,
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

def form_gameend(reply=False):
    return form_msg(msg_types[7], reply=reply)

def form_pickhero(myid, hero_ids, reply=True):
    return form_msg(msg_types[11], myid=myid, myhero=hero_ids, reply=reply)










if __name__ == '__main__':
    tep=form_msg('test')
    print(tep)
    print (type(json.loads(tep)))