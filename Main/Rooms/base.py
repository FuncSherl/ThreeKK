#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
from Common import Config,Message
import socket,json,random
import Persons,Cards
import threading

class base:
    def __init__(self, socket_list):
        self.socket_list=socket_list        
        self.heros_list=[None for i in range(len(self.socket_list))]  #存储英雄的id
        self.heros_instance=[None for i in range(len(self.socket_list))]
        self.campid=list( range(len(self.socket_list)) )
        
        self.cards_pile=self.generate_cards()
        self.cards_drop=[]
        
        self.game_status=True
        self.init_roomset()#加载房间设置 
        
    def init_roomset(self):
        self.allow_attack_cnt=1  #本房间的游戏方式，允许出几张杀，体现房间特性
        self.allow_armer=1  #允许几个武器
        self.allow_shield=1 #allow how many shield
        self.allow_horse=1
        
    def get_cards(self, cnt=1):
        #当发牌时
        if len(self.cards_pile)>=cnt:
            ret=self.cards_pile[:cnt]
            self.cards_pile=self.cards_pile[cnt:]
            return ret
        else:
            if len(self.cards_drop) >0:
                random.shuffle(self.cards_drop)
                self.cards_pile.extend(self.cards_drop)
                self.cards_drop=[]
            else:
                print ("add new pile of cards") #加一副牌
                self.cards_pile.extend(self.generate_cards())
            return self.get_cards(cnt)
    
    def drop_cards(self, cards_droped):
        #出过的牌
        self.cards_drop.extend(cards_droped)   
        return True           
            
    
    def generate_cards(self):
        #[ [cardid, color, num],...]
        #生成一副牌，根据牌的种类及各类中的各颜色的数目，随机分配点数
        kep_card_colors=[[] for x in range(len(Config.Card_color_enum))]
        for indi, i in enumerate(Cards.class_list):
            for indj,j in enumerate(i.cards_num_color):
                if indj >= len(Config.Card_color_enum): break #防止越接 
                for k in range(j):
                    kep_card_colors[indj].append([indi, indj])
        #print (kep_card_colors)
        ret=[]
        for i in kep_card_colors:
            #random.shuffle(i)
            for indj,j in enumerate(i):
                tep_ind=indj%(Config.Card_num_max-Config.Card_num_min+1)+Config.Card_num_min
                j.append(tep_ind)
            ret.extend(i)
        random.shuffle(ret)
        return ret
    
    def send_recv(self, c_sock, msg=None):
        '''
        :等待回复
        :若msg不为空则先发送msg
        '''
        if msg: self.send_message_str(c_sock, msg)
        try:
            tmsg=c_sock.recv(Config.BuffSize)
            
            if not tmsg: return None
            print ('recv:',tmsg)  #DEBUG
        except  socket.timeout:
            print ('ERROR:detected timeout')
            return None
        except Exception as e:
            print ('unexpected error:', str(e))
            return None
        msg_list_str=tmsg.decode('utf-8')
        msg_list=msg_list_str.split(Config.Message_tail)
        ret=[json.loads(x) for x in msg_list if x]
        return ret
    
    @classmethod
    def send_map_str(cls, socket, messagemap):
        # 统一处理发送map 形式的消息, 注意输入的messagemap为type：dict
        strm=json.dumps(messagemap)
        strm+=Config.Message_tail
        try:
            res=socket.send(strm.encode('utf-8'))
            print ('send:',strm) #DEBUG
        except Exception as e:
            print ('send error:', str(e))
            return None
        return res
    
    @classmethod
    def send_message_str(cls, socket, strm):
        # 统一处理发送string形式的消息, 注意输入的messagemap为type：string
        #strm=json.dumps(messagemap)
        strm+=Config.Message_tail
        try:
            res=socket.send(strm.encode('utf-8'))
            print ('send:',strm) #DEBUG
        except Exception as e:
            print ('send error:', str(e))
            return None
        return res
    
    def send_recv_onebyone(self, sock_list, msg_want=[], msg=None):
        ret=[None]*len(sock_list)
        
        for ind,i in enumerate(sock_list):
            tep=self.send_recv(i, msg)
            if not tep: continue
                        
            for j in tep:                
                if msg_want and j['msg_name'] not in msg_want: continue                
                ret[ind]=j
        return ret
    
    def send_msg_to_all(self, msg, replylist=[]):
        origin_reply=msg['reply']   #使用这个保存原来消息中的reply，如果改消息为全部回答的，只要msg中reply=True就行，不用填充replylist
        for ind,i in enumerate(self.socket_list):
            msg['myid']=ind  #第几个玩家
            msg['heros']=  [[self.heros_list[x], self.heros_instance[x].health if self.heros_instance[x] else None]  for x in range(len(self.heros_list))] #
            msg['cards']=[x.all_the_cards_holders() if x else None   for x in self.heros_instance]
            for inj,j in enumerate(msg['cards']):  
                if j and ind!=inj: j[0]=[None]*len(j[0])
            
            #print ((ind in replylist),  msg['reply'])   #DEBUG            
            msg['reply']=(ind in replylist) or origin_reply
            
            res=self.send_map_str(i, msg)
            
    def send_heartbeat_to_all(self, reply=False):
        msg=Message.form_heartbeat(reply=reply)
        self.send_msg_to_all(msg)
        if reply:
            ret=self.send_recv_onebyone(self.socket_list, [Message.msg_types[0]])
            for ind,i in enumerate(ret):
                if not ret: print ('Player %2d droped'%ind)
            
    #游戏中用到的一些事件
    def on_gamestart(self):  #1
        msg=Message.form_gamestart(0)
        print (msg)
        self.send_msg_to_all(msg)
        
            
    def on_gameend(self):
        msg=Message.form_gameend(0)
        self.send_msg_to_all(msg)
    
    def on_pickhero(self):  #2
        Config.HerosforSelect=min(int(len(Persons.class_list)/len(self.socket_list)), Config.HerosforSelect)
        Config.HerosforSelect=max(Config.HerosforSelect, 1)#这里防止可选英雄太少，导致错误,如果每人一个都还少那就没办法了
        
        cnt_ned=len(self.socket_list)*Config.HerosforSelect
        hero_list=random.sample(list( range( len(Persons.class_list) )), cnt_ned)
        for ind,i in enumerate(self.socket_list):
            msg=Message.form_pickhero(ind,  hero_list[ind*Config.HerosforSelect:(ind+1)*Config.HerosforSelect] , reply=True )
            self.send_map_str(i, msg)
        
        ret=self.send_recv_onebyone(self.socket_list, [Message.msg_types[11]])
        for ind,i in enumerate(ret):
            if i and i['heros'] and (i['heros'][0] in hero_list[ind*Config.HerosforSelect:(ind+1)*Config.HerosforSelect]):
                self.heros_list[ind]=i['heros'][0]                
            else: self.heros_list[ind]=hero_list[ind*Config.HerosforSelect]  
                         
            self.heros_instance[ind]=  Persons.class_list[self.heros_list[ind] ](self, ind)
            print ('Player ',ind, ' select ',self.heros_instance[ind].name)
        #到这里已经英雄选择完成
        
    def on_gameinited(self): #3
        #初始时游戏信息
        for i in self.heros_instance:
            i.addcard(self.get_cards(Config.Cardsforinit))
        
        msg=Message.form_gameinited(0, 0, 0, 0,  reply=False)
        self.send_msg_to_all(msg)
        
            
    def on_getcard(self, cnt, end, start=None,  public=False,  reply=False):
        if not start: cards_tep=self.get_cards(cnt)
        else: 
            cnt=min(cnt, len(self.heros_instance[start].cards))
            sel=random.sample(    range( len(self.heros_instance[start].cards) ), cnt)
            cards_tep=[self.heros_instance[start].cards[j] for j in sel]

            self.heros_instance[start].cards = [self.heros_instance[start].cards[i] for i in range(len(self.heros_instance[start].cards)) if (i not in sel)]

        
        for ind,i in enumerate(self.socket_list):
            tep=[None]*cnt
            if public or ind==end: tep=cards_tep
            
            heros=[[self.heros_list[x], self.heros_instance[x].health if self.heros_instance[x] else None]  for x in range(len(self.heros_list))]
            cards=[x.all_the_cards_holders() if x else None   for x in self.heros_instance]
            for inj,j in enumerate(cards):  
                if j and ind!=inj: j[0]=[None]*len(j[0])
            
            msg=Message.form_getcard(ind, heros, cards, [end],([start] if start else None), tep, reply=( (ind==end) and reply))
            self.send_map_str(i, msg)
        
        self.heros_instance[end].addcard(cards_tep)
        
    ############################################################################################
    
    def roundstart(self, startid): #4
        msg=Message.form_roundstart(None, None, None, startid, reply=False)
        self.send_msg_to_all(msg)
        
        self.heros_instance[startid].roundstart()        
        #以上完成回合开始时的准备工作
        
    def playcardstart(self, startid):     #5       
        #playcard(self, cardtoselect, selectcnt=1, inform='出牌阶段', end=None, 
        
        self.heros_instance[startid].playcardstart()
            
            
    def roundend(self, startid):#6
        msg=Message.form_roundend(None, None, None, startid, reply=False)
        self.send_msg_to_all(msg)
        self.heros_instance[startid].roundend()
        
        
    def gamestatus_judge(self):
        #return 继续游戏？
        tep=[self.campid[x] for x in range(len(self.heros_instance)) if (self.heros_instance[x].alive)]
        if max(tep)==min(tep):
            self.game_status=False
            return False
        return True
    
    
    
    #main function
    def start(self):
        print ('Room starting at thread:',threading.current_thread().getName())
        
        self.on_gamestart()
        self.on_pickhero()
        self.on_gameinited()
        
        st=random.randint(0, len(self.socket_list)-1)
        while self.game_status:
            print ('player:',st,'->',self.heros_instance[st].name,' round start!')
            if self.heros_instance[st].alive and self.game_status: self.roundstart(st)
            if self.heros_instance[st].alive and self.game_status: self.playcardstart(st)
            if self.heros_instance[st].alive and self.game_status: self.roundend(st)
            print ('next player round')
            if not self.gamestatus_judge(): break
            st+=1
            st%=len(self.socket_list)
            
        self.on_gameend()
        print ('Room end at thread:',threading.current_thread().getName())








if __name__ == '__main__':
    print (Persons.class_list)
    print (Cards.class_list)
    tep=base([0,1])
    print (tep.cards_pile)
    print (len(tep.cards_pile))










