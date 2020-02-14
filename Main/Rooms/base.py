#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
from Common import Config,Message
import socket,json,random
import Persons,Cards

class base:
    def __init__(self, socket_list):
        self.socket_list=socket_list        
        self.heros_list=[]
        self.cards_pile=self.generate_cards()
        self.cards_drop=[]
        
    def get_cards(self, cnt=1):
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
        self.cards_drop.extend(cards_droped)              
            
    
    def generate_cards(self):
        #[ [cardid, color, num],...]
        kep_card_colors=[[] for x in range(len(Config.Card_color_enum))]
        for indi, i in enumerate(Cards.class_list):
            for indj,j in enumerate(i.cards_num_color):
                if indj >= len(Config.Card_color_enum): break #防止越接 
                for k in range(j):
                    kep_card_colors[indj].append([indi, indj])
        #print (kep_card_colors)
        ret=[]
        for i in kep_card_colors:
            random.shuffle(i)
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
        if msg is not None: c_sock.send(msg)
        try:
            tmsg=c_sock.recv(Config.BuffSize)
            if not tmsg: return None
            
        except  socket.timeout:
            print ('detected timeout')
            return None
        except:
            print ('unexpected error')
            return None
        return json.loads(tmsg)
    
    def send_recv_onebyone(self, sock_list, msg_want, msg=None):
        ret=[]
        idcnt=0
        while idcnt<len(sock_list):
            tep=self.send_recv(sock_list[idcnt], msg)
            if tep and tep['msg_name']!=msg_want: continue
                
            ret.append(tep)
            idcnt+=1

        return ret
                
    def send_all(self, sock_list, msg):
        for i in sock_list:  i.send(msg)
            
    #游戏中用到的一些事件
    def on_gamestart(self):
        for ind, i in enumerate(self.socket_list):
            msg=Message.form_gamestart(ind, reply=False)
            i.send(msg)
            
    def on_gameend(self):
        msg=Message.form_gameend(reply=False)
        self.send_all(self.socket_list, msg)
    
    def on_pickhero(self):
        cnt_ned=len(self.socket_list)*Config.HerosforSelect
        hero_list=random.sample(range( len(Persons.class_list) ), cnt_ned)
        for ind,i in enumerate(self.socket_list):
            msg=Message.form_pickhero(ind,  hero_list[ind*Config.HerosforSelect:(ind+1)*Config.HerosforSelect] , reply=True )
            i.send(msg)
        
        ret=self.send_recv_onebyone(self.socket_list, Message.msg_types[11])
        for ind,i in enumerate(ret):
            if not i:
                self.heros_list.append(hero_list[ind*Config.HerosforSelect])
            else:
                self.heros_list.append(i['myhero'][0])
        #到这里已经英雄选择完成
        
    
    
    
    
    
    
    
    
    
    
    
    #main function
    def start(self):
        self.on_gamestart()
        
    
    










if __name__ == '__main__':
    print (Persons.class_list)
    print (Cards.class_list)
    tep=base([0,1])
    print (tep.cards_pile)
    print (len(tep.cards_pile))










