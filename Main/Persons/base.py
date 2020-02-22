#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
import socket
import sys,json
from Common import Config,Message
import Cards

class base:
    name='base'
    describ='base class'
    
    describ_skill1=''
    describ_skill2=''
    
    blood=4
    
    def __init__(self, room, pid):
        self.room=room
        self.playerid=pid   #玩家的id，即数组中的下标 
        self.mysocket=self.room.socket_list[pid]    #记录一下本实例中的socket
        
        self.alive=True
        self.health=self.blood
        self.cards=[] #[[], ]
        self.round_init()
        self.round_status=False
        self.function_table=Message.make_msg2fun(self)
        
        self.cards_may_play=[]
        self.cards_num_play=1
        self.cards_inform=''
        self.cards_end_may=None
        
        self.armer=[]
        self.shield=[]
        self.horse_minus=[]
        self.horse_plus=[]
        
        self.all_the_cards_holders=lambda :[self.cards, self.armer, self.shield, self.horse_minus, self.horse_plus]
        
        
    def round_init(self):
        self.attack_cnt=0
        self.failer_cnt=0
        self.round_status=True  #回合未结束
        
        self.round_additional_damage_attack=0#本回合的附加伤害
        self.next_additional_damage_attack=0#下一次基本牌的附加伤害
        
        self.round_additional_damage_skill=0#本回合技能附加伤害
        self.next_additional_damage_skill=0#下一次技能附加伤害
        
        
        
    #这里体现各种技能
    def roundstart(self):
        self.round_init()
        #没有技能情况下就是摸2张牌，这里room.getcard可以从玩家手中摸牌，此时start为被摸牌的玩家 
        self.room.on_getcard( Config.Cardeachround, end=self.playerid, start=None,  public=False,  reply=False)
        
    def roundend(self):
        if len(self.cards)>self.health:      
            #启动弃牌
            dropcnt=len(self.cards)-self.health
            
            msg=Message.form_roundend_dropcard(0, 0, 0, self.playerid, dropcnt, reply=False)
            self.room.send_msg_to_all(msg, replylist=[self.playerid])
                
            if not self.listen_distribute([Message.msg_types[13]]):
                dropedcards=self.cards[:dropcnt]
                self.cards=self.cards[dropcnt:]
                self.room.drop_cards(dropedcards)     
        self.round_status=False           
        return True
    
    
    def drophealth(self, person_start, damage):
        #掉血响应
        if person_start.dodamage(self, damage):
            self.health-=damage
            if self.health<=0:
                self.ask_for_save()
            #后面如果还血量不够，就死亡
            if self.health<=0:
                self.ondeath()
            
            
    
    def before_dodamage(self, person_end, damage):
        #return true表示person_end可以因掉血发动技能
        
        return True
    
    def after_dodamage(self, person_end, damage):
        
        return True
    
    def ondeath(self):
        self.alive=False
        for i in self.all_the_cards_holders():
            self.room.drop_cards(i)
    
    
    def activecards(self):
        #当前的牌中有哪些是可以主动出的
        ret=[]
        for i in self.cards:
            if Cards.class_list[i[0]].cal_active(self):
                #张飞可不用下面这句判断 
                if Cards.class_list[i[0]].name=='杀' and self.attack_cnt>=self.room.allow_attack_cnt:continue
                ret.append(i)
        return ret
            
        
    ##############################################################################
    
    def listen_distribute(self, msgwant=[]):
        msg=self.room.send_recv(self.mysocket)
        if msg:
            if msgwant and msg['msg_name'] not in msgwant: return self.listen_distribute(msgwant)
            return self.function_table[msg['msg_name']](msg)
        else:
            return None
    
    def playcard(self, cardtoselect, selectcnt=1, inform='出牌阶段', end=None):
        #告诉所有人谁正在选牌出,其中end为None表示由玩家选择目标，目标合理性判断由牌+玩家决定；如果有list，则目标必须在end的list中 
        msg=Message.form_askselect(0, 0, 0, self.playerid, end, inform, cardtoselect, select_cnt=selectcnt, reply=False)
        self.room.send_msg_to_all(msg, replylist=[self.playerid])
        
            
        self.cards_may_play=cardtoselect
        self.cards_num_play=selectcnt
        self.cards_inform=inform
        self.cards_end_may=end
        
        return self.listen_distribute([Message.msg_types[1], Message.msg_types[14]])
        
    def addcard(self, cards_list):
        self.cards.extend(cards_list)
        
    def dropcard(self, cards_list):
        for i in cards_list:
            for j in self.all_the_cards_holders():
                if i in j: j.remove(i)
        #for i in cards_list: self.cards.remove(i)  #出牌了
        
    def cal_distance(self, startplayerid, endplayerid):
        tep=abs(endplayerid-startplayerid)
        dis=min(tep, len(self.room.socket_list)-tep  )
        if self.room.heros_instance[startplayerid].horse_minus:  dis-=1
        if self.room.heros_instance[endplayerid].horse_plus:  dis+=1
        return dis
    
    def cal_armerlength(self, card):
        #[cardid, color, num]
        cardid=card[0]
        tmax=Cards.class_list[cardid].scop
        if self.armer and Cards.class_list[cardid].name=='杀':            
            for i in self.armer:
                tmax=max(tmax, Cards.class_list[i[0]].scop)
        return tmax
    
    
    def ask_for_save(self):
        pass
    
    
    #下面为消息响应区 ，该部分的函数应该与Messge中的一致，注意这里为收到消息的响应，其驱动为收到消息
    def on_heartbeat(self, msg):
        return True
    
    def judge_playcard(self, cards, ed):
        #当收到玩家打出一张牌时，根据出牌时的状态判断该牌出的是否合理 
        if len(cards) != self.cards_num_play:  return False
            
        for i in cards:
            if i not in self.cards_may_play:       return False
            
        if self.cards_end_may is None:#判定牌的目标合理性,None表示根据牌来定，list则目标必须在相等
            for i in ed:
                for j in cards:
                    if i not in Cards.class_list[ j[0] ].cal_targets: return False            
        else:
            return ed==self.cards_end_may
            '''
            for i in ed: 
                if i not in self.cards_end_may: return False
            '''
        
        return True
    
    def playcard_drop(self, cards):
        #当该玩家打出牌时，该函数负责处理弃牌等操作，基本牌直接弃牌，装备牌可以替换
        dropcards=[]
        for i in cards:
            tep=Cards.class_list[ i[0] ].type
            if tep==Config.Card_type_enum[0] or tep==Config.Card_type_enum[1]:#['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
                dropcards.append(i)                
            elif tep==Config.Card_type_enum[2]:                
                self.armer.append(i)
                if len(self.armer)>self.room.allow_armer: dropcards.extend(self.armer[:-self.room.allow_armer])
            elif tep==Config.Card_type_enum[3]:                
                self.shield.append(i)
                if len(self.shield)>self.room.allow_shield: dropcards.extend(self.shield[:-self.room.allow_shield])
            elif tep==Config.Card_type_enum[4]:
                dropcards.extend(self.horse_minus)
                self.horse_minus=[i]
            elif tep==Config.Card_type_enum[5]:
                dropcards.extend(self.horse_plus)
                self.horse_plus=[i]
            else:
                print('error:unkonwn card type')
        self.dropcard(dropcards)
        self.room.drop_cards(dropcards) #牌进入弃牌堆

                
                
    
    def on_playcard(self, msg):
        #重要处理，很多情况下这里因该收到该消息,即用户打出一张牌
        cards=msg['third']
        st=self.playerid #msg['start']
        ed=msg['end']        
        
        if not self.judge_playcard(cards, ed): 
            self.failer_cnt+=1  #限制出牌失败次数
            if self.failer_cnt>=Config.FailerCnt:return False
            return  self.playcard(self.cards_may_play, self.cards_num_play, self.cards_inform, self.cards_end_may)            
        #到这说明出牌没问题
        #self.dropcard(cards)
        #self.room.drop_cards(cards) #牌进入弃牌堆 
        self.playcard_drop(cards)
        
        msg=Message.form_playcard(0, 0, 0, st, ed, cards, reply=False)  #通知所有人谁向谁出了牌
        self.room.send_msg_to_all(msg)
        
        for i in ed:
            for j in cards:
                #将控制权交给该牌
                tesu=Cards.class_list[ j[0] ].on_be_playedto(self, self.room.heros_instance[i])
                #命中
                if not tesu: 
                    for k in self.armer:
                        # 武器牌的命中效果不一样,这里添加额外伤害什么的
                        arm_resu=Cards.class_list[ k[0] ].on_hit_player( self, self.room.heros_instance[i])
                    if arm_resu: pass
                    #以杀为例，这里命中时造成伤害
                    Cards.class_list[ j[0] ].on_hit_player( self, self.room.heros_instance[i])
                    break  #命中一个人一次得了 
                
        #不管如何应对，这里出牌是成功的
        return True
    
    def on_judgement(self, msg):
        return False
    
    def on_getcard(self, msg):
        return False
    
    def on_roundstart(self, msg=None):
        return False
        
    def on_roundend(self, msg=None):
        return False            
        
    def on_gamestart(self, msg):
        return False
    
    def on_gameend(self, msg):
        return False
    
    def on_skillstart(self, msg):
        return False
    
    def on_equipstart(self, msg):
        return False
    
    def on_inform_beforegame(self, msg):
        return False
    
    def on_pickhero(self, msg):
        return False
    
    def on_gameinited(self, msg):
        return False
    
    def on_roundend_dropcard(self, msg):
        dropedcards=[self.cards[x]  for x in msg['third']]
        self.cards=[self.cards[x]  for x in range(len(self.cards)) if (x not in msg['third'])]
        self.room.drop_cards(dropedcards)
        
        return True
        
    
    def on_askselect(self, msg):
        #返回的msg中third中为用户选择，forth为选择的card，
        #return False
        if not msg['third'] or not msg['third'][0]:
            return False
        return msg['forth']
        

    
    

if __name__ == '__main__':
    pass













