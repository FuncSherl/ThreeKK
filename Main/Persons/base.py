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
    describ_skill3=''
    describ_skill4=''
    
    describ_skill_list=[describ_skill1, describ_skill2, describ_skill3, describ_skill4]
    
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
        self.cards_end_num=0
        
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
        
        
    ##########################################################################################################
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
    
    def addhealth(self, person_start, health_add=1, card=None):        
        self.health=min( self.blood, self.health+health_add)
        return True
    
    
    def drophealth(self, person_start, damage, card):
        #如果before_dodamage-》before_damaged-》受伤-》after_dodamage-》after_damaged        
        #掉血响应
        if person_start.before_dodamage(self, damage, card):
            damage=self.before_damaged( person_start, damage, card)
            self.health-=damage
            if self.health<=0:
                self.ask_for_save()
            #后面如果还血量不够，就死亡
            if self.health<=0:
                self.ondeath()
            
            if person_start.after_dodamage(self, damage, card):
                self.after_damaged(person_start, damage, card)
    
    def before_playcards(self, cards):
        pass
    
    def after_playcards(self, cards):
        pass
    
    def add_armer(self, card):
        self.armer.append(card)
        if len(self.armer)>self.room.allow_armer:
            dropcards=self.armer[:-self.room.allow_armer]
            self.armer=self.armer[-self.room.allow_armer:]
            #self.room.drop_cards(dropcards)
        
    
    def add_shield(self, card):
        self.shield.append(card)
        if len(self.shield)>self.room.allow_shield:
            dropcards=self.shield[:-self.room.allow_shield]
            self.shield=self.shield[-self.room.allow_shield:]
            #self.room.drop_cards(dropcards)
            
    def add_horse_minus(self, card):
        self.horse_minus.append(card)
        if len(self.horse_minus)>self.room.allow_horse:
            dropcards=self.horse_minus[:-self.room.allow_horse]
            self.horse_minus=self.horse_minus[-self.room.allow_horse:]
            #self.room.drop_cards(dropcards)
            
    def add_horse_plus(self, card):
        self.horse_plus.append(card)
        if len(self.horse_plus)>self.room.allow_horse:
            dropcards=self.horse_plus[:-self.room.allow_horse]
            self.horse_plus=self.horse_plus[-self.room.allow_horse:]
            #self.room.drop_cards(dropcards)
        
    
    def before_dodamage(self, person_end, damage, card):
        #
        
        return True
    
    def after_dodamage(self, person_end, damage, card):
        
        return True
    
    
    #自己掉血时
    def before_damaged(self, person_start, damage, card):
        #return true表示person_end可以因掉血发动技能
        return self.ask_shield_before_damage(damage)
        
    
    def after_damaged(self, person_start, damage, card):
        #掉血技能
        
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
            
        
    ##############################################################################################################
    #以下为工具函数，每个类中相同，不必重写
    def listen_distribute(self, msgwant=[]):
        msg=self.room.send_recv(self.mysocket)
        if msg:
            if msgwant and msg['msg_name'] not in msgwant: return self.listen_distribute(msgwant)
            return self.function_table[msg['msg_name']](msg)
        else:
            return None
        
    def ask_armers_before_playcard(self):
        #出牌前询问武器技能发动,return True表示继续后面的出牌进程，否则重新开始出牌
        for i in self.armer:
            res=Cards.class_list[i[0]].before_playcard(self)
            if not res: return False
        return True
    
    def ask_shield_before_damage(self, damage):
        ret=damage
        for i in self.shield:
            ret=min(ret, Cards.class_list[i[0]].on_damaged(damage))
        return ret
    
    def judge_playcard(self, cards, ed):
        #当收到玩家打出一张牌时，根据出牌时的状态判断该牌出的是否合理 
        if len(cards) != self.cards_num_play:  return False
            
        for i in cards:
            if i not in self.cards_may_play:       return False
            
        if self.cards_end_may is None:#判定牌的目标合理性,None表示根据牌来定
            for i in cards:
                tn,endids=Cards.class_list[ i[0] ].cal_targets(self)
                tn+=self.cards_end_num
                if len(ed)>tn:return False
                for j in ed:
                    if j not in endids: return False           
        else:
            if len(ed)>self.cards_end_num: return False
            for i in ed:
                if i not in self.cards_end_may: return False
            '''
            for i in ed: 
                if i not in self.cards_end_may: return False
            '''
        
        return True
    
    def playcard(self, cardtoselect, selectcnt=1, inform='出牌阶段', end=None, endnum=0, active=True, go_on=True):
        #告诉所有人谁正在选牌出,其中end为None表示由玩家选择目标，目标合理性判断由牌+玩家决定；如果有list，则目标必须在end的list中 
        #active表示是否是先手方，或者是被动出牌        endnum仅参考，给出目标的上限数目
        self.cards_may_play=cardtoselect
        self.cards_num_play=selectcnt
        self.cards_inform=inform
        self.cards_end_may=end
        self.cards_end_num=endnum
        
        #这里发动装备 
        if active:  
            if not  self.ask_armers_before_playcard(): return True
                   
        msg=Message.form_askselect(0, 0, 0, self.playerid, end, inform, cardtoselect, select_cnt=selectcnt, reply=False)
        self.room.send_msg_to_all(msg, replylist=[self.playerid])
        
        ####################
        msg= self.listen_distribute([Message.msg_types[1], Message.msg_types[14]])
        if not msg: return False
        
        #重要处理，很多情况下这里因该收到该消息,即用户打出一张牌
        cards=msg['third']
        st=self.playerid #list(set(msg['start']))
        ed=list(set(msg['end']   ))     
        
        if not self.judge_playcard(cards, ed): 
            self.failer_cnt+=1  #限制出牌失败次数
            if self.failer_cnt>=Config.FailerCnt:return False
            return  self.playcard(cardtoselect, selectcnt, inform, end, endnum, active)            
        
        
        #出牌没问题
        self.dropcard(cards)
        
        if active:
            self.before_playcards(cards)
        
        msg=Message.form_playcard(0, 0, 0, st, ed, cards, reply=False)  #通知所有人谁向谁出了牌
        self.room.send_msg_to_all(msg)
        
        #将控制权交给该牌
        if go_on:
            for k in ed:
                for i in cards: 
                    tesu=Cards.class_list[ i[0] ].on_be_playedto(self, self.room.heros_instance[k], i)
                    #返回是否命中
                    if tesu: break  #命中一次可以了
        if active:
            self.after_playcards(cards)
                
        #不管如何应对，这里出牌是成功的
        return cards
        
        
    def addcard(self, cards_list):
        self.cards.extend(cards_list)
        
    def dropcard(self, cards_list):
        for i in cards_list:
            if i in self.cards: 
                self.cards.remove(i)
                self.room.drop_cards([i]) #牌进入弃牌堆
                
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

                
                
    
    def on_playcard(self, msg):
        return msg
        
    
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













