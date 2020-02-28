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
    name_pinyin='base'
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
        self.msg_queue=[]
        
        self.cards_may_play=[]
        self.cards_num_play=1
        self.cards_inform=''
        self.cards_end_may=None
        self.cards_end_num=0
        
        self.armer=[]
        self.shield=[]
        self.horse_minus=[]
        self.horse_plus=[]
        self.delayed_skill=[]
        
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
                self.dropcard(dropedcards)    
        self.round_status=False           
        return True
                  
    ###############################################################################出牌的各个时间点的处理            
    def playcardstart(self):
        #如果英雄一开始出牌可以选择其他，这里要修改,eg.guanyu
        while self.playcard(self.activecards()):#出牌超时，出牌阶段结束
            #新一轮出牌,每次循环都是代表一张牌已经处理完了，比如决斗相互出牌处理完了，这里等待出一张新牌
            #这样则必须在下次循环前将该牌的相关处理完
            pass
    
    def init_playcards(self, card=None):  #可以进行判断最后一张手牌等操作
        if not  self.ask_armers_init_playcard(card): return False
        if not  self.ask_shields_init_playcard(card): return False
        return True
    
    
    def before_playcards(self, endperson, card):    #出牌前进行装备判断，对某张牌进行加成
        if not  self.ask_armers_before_playcard(endperson, card): return False
        if not  self.ask_shields_before_playcard(endperson, card): return False
        return True
    
    def on_be_playcard(self, startperson, card):
        if not self.ask_shield_on_attacked(startperson, card): return False
        if not self.ask_armer_on_attacked(startperson, card): return False
        #被chupai时的技能
        
        return True
    
    def after_playcard(self,endperson, card, hit=False):   #出牌后的装备技能判断，对
        if not self.ask_shield_after_playcard(endperson, card, hit): return False
        if not self.ask_armer_after_playcard(endperson, card, hit): return False
        #被chupai时的技能
        
        return True
    
    def play_one_card(self, endperson, card, active):
        #return True: normal  False: break
        if self.before_playcards(endperson, card): #只有出牌方同意
            if not endperson.on_be_playcard(self, card):  #被出牌方才能进行盾牌的格挡判断 
                return True   
        #这后面的处理就不要考虑装备效果了， 在牌各自的处理中只处理自己的事
        tesu=Cards.class_list[ card[0] ].on_be_playedto(self, endperson, card)
        #返回是否命中  tesu=True 命中        
                    
        if active:#如果未命中，可以发动一些装备
            if not self.after_playcard(endperson, card, tesu): return False
        
        if tesu: return False  #命中一次可以了
        return True
    
    ######################################################################################新装备来到处理 
    def add_armer(self, card):
        self.armer.append(card)
        if card in self.room.cards_drop: self.room.cards_drop.remove(card)
        if len(self.armer)>self.room.allow_armer:
            dropcards=self.armer[:-self.room.allow_armer]
            self.armer=self.armer[-self.room.allow_armer:]
            self.room.drop_cards(dropcards)
        
    
    def add_shield(self, card):
        self.shield.append(card)
        if card in self.room.cards_drop: self.room.cards_drop.remove(card)
        if len(self.shield)>self.room.allow_shield:
            dropcards=self.shield[:-self.room.allow_shield]
            self.shield=self.shield[-self.room.allow_shield:]
            self.room.drop_cards(dropcards)
            
    def add_horse_minus(self, card):
        self.horse_minus.append(card)
        if card in self.room.cards_drop: self.room.cards_drop.remove(card)
        if len(self.horse_minus)>self.room.allow_horse:
            dropcards=self.horse_minus[:-self.room.allow_horse]
            self.horse_minus=self.horse_minus[-self.room.allow_horse:]
            self.room.drop_cards(dropcards)
            
    def add_horse_plus(self, card):
        self.horse_plus.append(card)
        if card in self.room.cards_drop: self.room.cards_drop.remove(card)
        if len(self.horse_plus)>self.room.allow_horse:
            dropcards=self.horse_plus[:-self.room.allow_horse]
            self.horse_plus=self.horse_plus[-self.room.allow_horse:]
            self.room.drop_cards(dropcards)
            
            
    def add_delayed_skill(self, card):
        self.delayed_skill.append(card)
        if card in self.room.cards_drop: self.room.cards_drop.remove(card)
        
        
    ###########################################################################################生命值处理部分 
    def addhealth(self, person_start, health_add=1, card=None):        
        self.health=min( self.blood, self.health+health_add)
        return True
    
         
    def drophealth(self, person_start, damage, card):
        #如果before_dodamage-》before_damaged-》受伤-》after_dodamage-》after_damaged        
        #掉血响应
        damage=person_start.before_dodamage(self, damage, card) #伤害来源允许才能进行向下进行
        if damage:
            damage=self.before_damaged( person_start, damage, card) #装备效果和技能
            self.health-=damage
            if self.health<=0:
                self.ask_for_save()
            #后面如果还血量不够，就死亡
            if self.health<=0:
                if not self.ondeath(): return damage
            
            if person_start.after_dodamage(self, damage, card):  #伤害来源允许才能发动掉血技能
                self.after_damaged(person_start, damage, card)  #发动掉血技能
        return damage
    #A.before_dodamage->self.before_damaged->drop health->A.after_dodamage->self.after_damaged
    def before_dodamage(self, endperson, damage, card):
        #
        damage= self.ask_armer_before_dodamage(self, endperson, damage, card)
        damage= self.ask_shield_before_dodamage(self, endperson, damage, card)
        return max(0, damage)
    
    def after_dodamage(self, person_end, damage, card):
        #造成伤害后技能
        
        return True
    
    
    #自己掉血时
    def before_damaged(self, person_start, damage, card):
        #return true表示person_end可以因掉血发动技能
        damage=self.ask_shield_on_damaged(person_start,damage, card)
        damage=self.ask_armer_on_damaged(person_start,damage, card)
        return max(0, damage)
    
    def after_damaged(self, person_start, damage, card):
        #掉血技能
        
        return True
    
    ###################################################################    
    def ondeath(self):
        self.alive=False
        for i in self.all_the_cards_holders():
            self.room.drop_cards(i)
    
    
    ####################################################################
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
        self.function_table=Message.make_msg2fun(self)
        
        while self.msg_queue:
            name=self.msg_queue[0]['msg_name']
            if msgwant and name not in msgwant: self.msg_queue.pop(0)
            else: return self.function_table[name](self.msg_queue.pop(0))
        
        msg_list=self.room.send_recv(self.mysocket)
        
        if not msg_list: return msg_list
        
        self.msg_queue.extend(msg_list)

        return self.listen_distribute(msgwant)
        
    ###################################################################  每次准备出牌前的处理,如添加可选择的目标数目
    def ask_armers_init_playcard(self, card=None):
        #出牌前询问武器技能发动,return True表示继续后面的出牌进程，否则重新开始出牌
        for i in self.armer:
            res=Cards.class_list[i[0]].init_playcard(self, card)
            if not res: return False
        return True
    
    def ask_shields_init_playcard(self, card=None):
        #出牌前询问盾技能发动,return True表示继续后面的出牌进程，否则重新开始出牌
        for i in self.shield:
            res=Cards.class_list[i[0]].init_playcard(self, card)
            if not res: return False
        return True    
    
    ###################################################################  要打出一张牌了
    def ask_armers_before_playcard(self, endperson, card=None):
        #出牌前询问武器技能发动,return True表示继续后面的出牌进程，否则重新开始出牌
        for i in self.armer:
            res=Cards.class_list[i[0]].before_playcard(self, endperson,card)
            if not res: return False
        return True
    
    def ask_shields_before_playcard(self, endperson, card=None):
        #出牌前询问盾技能发动,return True表示继续后面的出牌进程，否则重新开始出牌
        for i in self.shield:
            res=Cards.class_list[i[0]].before_playcard(self,endperson, card)
            if not res: return False
        return True
    ##############################################################################当有伤害来时
    def ask_shield_on_damaged(self, startperson, damage, card=None):
        ret=damage
        for i in self.shield:
            ret=min(ret, Cards.class_list[i[0]].on_damaged(self, startperson, ret,card))
        return ret
    
    def ask_armer_on_damaged(self, startperson, damage, card=None):
        ret=damage
        for i in self.armer:
            ret=min(ret, Cards.class_list[i[0]].on_damaged(self, startperson, ret, card))
        return ret
    
    ###############################################################################被攻击时，一般不会涉及武器    
    def ask_shield_on_attacked(self,  endperson,card):
        #return True没有挡住，继续处理，False被挡住了,不用处理
        for i in self.shield:
            res=Cards.class_list[i[0]].on_attacked(self, endperson,card)
            if not res: return False
        return True
    
    def ask_armer_on_attacked(self,  endperson,card):
        #return True没有挡住，继续处理，False被挡住了,不用处理
        for i in self.shield:
            res=Cards.class_list[i[0]].on_attacked(self, endperson,card)
            if not res: return False
        return True
    
    ###############################################################################before_dodamage   
    def ask_shield_before_dodamage(self,  endperson, damage,card):
        ret=damage
        for i in self.shield:
            ret=max(ret, Cards.class_list[i[0]].before_dodamage(self, endperson, ret,card) )
        return ret
    
    def ask_armer_before_dodamage(self, endperson, damage,card):
        ret=damage
        for i in self.armer:
            ret=max( ret, Cards.class_list[i[0]].before_dodamage(self, endperson, ret,card))
        return ret
    
    ###############################################################################被攻击时，一般不会涉及武器    
    def ask_shield_after_playcard(self,  endperson,card, hit):
        #return True没有挡住，继续处理，False被挡住了,不用处理
        for i in self.shield:
            res=Cards.class_list[i[0]].after_playcard(self, endperson,card, hit)
            if not res: return False
        return True
    
    def ask_armer_after_playcard(self,  endperson,card, hit):
        #return True没有挡住，继续处理，False被挡住了,不用处理
        for i in self.shield:
            res=Cards.class_list[i[0]].after_playcard(self, endperson,card, hit)
            if not res: return False
        return True
    
    ################################################################################
    def judge_playcard(self, cards, ed):
        #当收到玩家打出一张牌时，根据出牌时的状态判断该牌出的是否合理 
        if len(cards) != self.cards_num_play:  return False
            
        for i in cards:
            if i not in self.cards_may_play:       return False
        
        for i in ed: 
            if not self.room.heros_instance[i].alive: return False
        
        print (self.cards_end_may)
        if self.cards_end_may is None:#判定牌的目标合理性,None表示根据牌来定
            for i in cards:
                tn,endids=Cards.class_list[ i[0] ].cal_targets(self)
                if len(endids)==tn: continue  #这种情况下不用选择
                tmaxn=max(tn, max(self.cards_end_num) )  #有时可以选择多个目标，比原来的要多
                if len(ed)>tmaxn or len(ed)<=0:return False
                for j in ed:
                    if j not in endids: return False           
        else:
            if len(ed) not in self.cards_end_num: return False
            for i in ed:
                if i not in self.cards_end_may: return False
            '''
            for i in ed: 
                if i not in self.cards_end_may: return False
            '''
        
        return True
    
    def playcard(self, cardtoselect, selectcnt=1, inform='出牌阶段', end=None, endnum=[], active=True, go_on=True):
        #告诉所有人谁正在选牌出,其中end为None表示由玩家选择目标，目标合理性判断由牌+玩家决定；如果有list，则目标必须在end的list中 
        #active表示是否是先手方，或者是被动出牌        endnum仅参考，给出目标的上限数目
        self.cards_may_play=cardtoselect
        self.cards_num_play=selectcnt
        self.cards_inform=inform
        self.cards_end_may=end
        self.cards_end_num=endnum
        
        #这里发动装备 
        if active:  
            if not self.init_playcards(): return  False
            
        #myid, myheroid, mycards, start, end, informmsg, cardstoselect, select_cnt=1,  reply=True
        msg=Message.form_askselect(0, 0, 0, [self.playerid], self.cards_end_may, \
                                   self.cards_inform, self.cards_may_play, select_cnt=self.cards_num_play, reply=False)
        self.room.send_msg_to_all(msg, replylist=[self.playerid])
        
        ####################
        msg= self.listen_distribute([Message.msg_types[1], Message.msg_types[14]])
        if not msg: return False
        
        #重要处理，很多情况下这里因该收到该消息,即用户打出一张牌
        cards=msg['third']
        st=[self.playerid] #list(set(msg['start']))
        ed=list(set(msg['end']   ))     
        
        if not self.judge_playcard(cards, ed): 
            self.failer_cnt+=1  #限制出牌失败次数
            if self.failer_cnt>=Config.FailerCnt:return False
            return  self.playcard(cardtoselect, selectcnt, inform, end, endnum, active)            
        
        
        #出牌没问题
        # 既然已经出牌了，就先把牌弃掉，但是牌的信息还在，当后面添加装备时，在从弃牌堆里面删掉该牌
        self.dropcard(cards)
                
        msg=Message.form_playcard(0, 0, 0, st, ed, cards, reply=False)  #通知所有人谁向谁出了牌
        self.room.send_msg_to_all(msg)
        
        #将控制权交给该牌
        if go_on:
            for k in ed:
                for i in cards: 
                    if not self.play_one_card(self.room.heros_instance[k], i, active): break
                    '''
                    if self.before_playcards(self.room.heros_instance[k], i): #只有出牌方同意
                        if not self.room.heros_instance[k].on_be_playcard(self, i):  #被出牌方才能进行盾牌的格挡判断 
                            continue   
                    #这后面的处理就不要考虑装备效果了， 在牌各自的处理中只处理自己的事
                    tesu=Cards.class_list[ i[0] ].on_be_playedto(self, self.room.heros_instance[k], i)
                    #返回是否命中
                    if tesu: break  #命中一次可以了
                    
                    if active:#如果未命中，可以发动一些装备
                        if not self.after_playcards(self.room.heros_instance[k], i): break
                    '''
        #不管如何应对，这里出牌是成功的
        return [cards, ed]
        
        
    def addcard(self, cards_list):
        self.cards.extend(cards_list)
        
    def dropcard(self, cards_list):
        for i in cards_list:
            for j in self.all_the_cards_holders(): 
                if i in j:
                    j.remove(i)
                    self.room.drop_cards([i]) #牌进入弃牌堆
                    break
                    
        #for i in cards_list: self.cards.remove(i)  #出牌了
        
    def cal_distance(self, startplayerid, endplayerid):
        tep=abs(endplayerid-startplayerid)
        dis=min(tep, len(self.room.socket_list)-tep  )
        dis-=len(self.room.heros_instance[startplayerid].horse_minus)
        dis+=len(self.room.heros_instance[endplayerid].horse_plus)
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
        dropedcards=msg['third']
        self.dropcard(dropedcards)
    
        return True
        
    
    def on_askselect(self, msg):
        #返回的msg中third中为用户选择，forth为选择的card，
        #return False
        if not msg['third'] or not msg['third'][0]:
            return False
        return msg['forth']
        

    
    

if __name__ == '__main__':
    pass













