#coding:utf-8
'''
Created on 2020年2月26日

@author: sherl
'''
import os,math
import Cards,Persons,Rooms
from Rooms import base
from Common import Config,Message
from UI_Cmd.person import person 
import socket ,time
import sys,json,msvcrt
import eventlet
import numpy as np
import platform
syst = platform.system()
eventlet.monkey_patch()


class UI_cmd:        
    height=30-1  #cmd为30行
    width=120-2 #120列个字符
    

    user_stx=int(width/4)
    user_sty=int(height*4/5)
    
    playarea_y=person.mheight+10
    
    center_x=int(width/2)
    center_y=int(  (center_x**2 + user_sty**2)/ (2*user_sty)   )
    start_angle=math.acos(center_x*1.0/center_y)
    
    
    def __init__(self, ipstr='127.0.0.1'):
        self.ipstr=ipstr
        self.socket=self.connect_server(self.ipstr)

        self.pannel=[]
        for i in range(self.height):
            self.pannel.append([])
            for j in range(self.width):
                self.pannel[-1].append(' ')
        #最多支持6个人才不会重叠
        self.person_instance=[]
        self.myindex=None
        self.game_status=True
        #self.pannel[:,:]=ord(' ')
        #char->ascll ord('c')
        #ascll->char chr(97)
        #for i in self.pannel: print (''.join(i))
        #self.update()
        
        
        
    def draw_clients(self):
        descrs=[x.get_describe() for x in self.person_instance]  #这里必须先获取描述信息，目的是更新各个person对象中的mlen变量
        if not descrs: return
        #print (descrs)
        
        mlen=max( [x.mlen for ind,x in enumerate(self.person_instance)] )
        #r=int ((self.width-mlen)/2 )
        r=self.center_y
        angel=(math.pi-2*self.start_angle)/( len(self.person_instance))
        
        st=(self.myindex-1)%len(self.person_instance)
        for i in range(1, len(self.person_instance)):
            tx=int( self.center_x- math.cos(self.start_angle+i*angel)*r-self.person_instance[st].mlen/2 )
            ty=int( self.center_y- math.sin(self.start_angle+i*angel)*r)
            #descrs[st].insert(1, 'INDEX:%d'%st)
            self.draw_panel(descrs[st], ty, tx)
            
            self.person_instance[st].playcard_x=int( self.width/2-(self.width/2-tx)/2 )
            self.person_instance[st].playcard_y=int( (ty+self.user_sty)/2 )
            
            st=(st-1)%len(self.person_instance)
        
            
        
    def draw_me(self):
        if not self.person_instance:return
        desr=self.person_instance[self.myindex].get_describe()
        self.draw_panel(desr, self.height, self.width) #放到右下角，自动识别更改
        
    def draw_my_cards(self, cards_list):
        if not self.person_instance:return
        res=self.person_instance[self.myindex].form_all_cards(cards_list)
        mlen=self.person_instance[self.myindex].mlen
        mhight=self.person_instance[self.myindex].mhigh
        stx=0
        sty=self.height-mhight-1
        
        self.draw_panel(['*'*self.width], sty, stx)
        
        sty+=2
        
        for ind,i in enumerate(res):
            tstr=str(ind)+'>'+i+'    '
            if stx+len(tstr.encode('utf-8'))+mlen+1>self.width:
                stx=0
                sty+=2
            self.draw_panel([tstr], sty, stx)
            stx+=len(tstr.encode('utf-8'))
            
    def draw_play_cards(self, cards):
        descs=[person.form_card(x) for x in cards]
        mlen=max( [len(x) for x in descs] )
        stx=int((self.width-mlen)/2)
        self.draw_panel(descs, self.playarea_y-len(cards), stx)
        
        self.person_instance[self.myindex].playcard_x=int( self.width/2)
        self.person_instance[self.myindex].playcard_y=self.playarea_y-len(cards)-1
        
    def draw_link(self, sty, stx, edy, edx):
        kep_stx=stx
        kep_sty=sty
        inch_x=1 if edx>stx else -1
        inch_y=1 if edy>sty else -1
        while not (stx==edx and sty==edy):
            if abs(edy-sty)>abs(edx-stx):
                self.pannel[sty][stx]='|'
                sty+=inch_y
            elif abs(edy-sty)<abs(edx-stx):
                self.pannel[sty][stx]='-'
                stx+=inch_x
            else:
                self.pannel[sty][stx]='/'
                if (edy-sty)*(edx-stx)>=0: self.pannel[sty][stx]='\\'
        tep=None
        if abs(edy-kep_sty)>abs(edx-kep_stx): 
            tep='^'
            if edy>kep_sty:tep='v'
        else:
            tep='<'
            if edx>kep_stx: tep='>'
        self.pannel[sty][stx]=tep
            
    def normal_draw_all(self, cards_list):
        #正常对局下的每次打印
        self.draw_clients()
        self.draw_me()
        self.draw_my_cards(cards_list)
        
    def sel_hero_draw(self, heroidlist):
        desc_list=[person(y, 0).get_hero_describe() for y in heroidlist]
        mlist=[ max([len(x.encode('utf-8')) for x in y])  for y in desc_list]
        #gap=int(  (self.width-sum(mlist))  /  (len(heroidlist)+1) )
        
        stx=0
        sty=0
        for i in range(len(heroidlist)):
            #self.pannel[sty-2][stx+int( mlist[i]/2)]=str(i)
            #self.pannel[sty-1][stx+int( mlist[i]/2)]='V'
            desc_list[i].insert(1, 'INDEX:%d'%i)
            #stx+=gap
            self.draw_panel(desc_list[i], sty, stx)
            sty+=len(desc_list[i])
            #print(desc_list[i])
            
            
    def update(self, clean_pannel=True, cards=None):
        self.clean_screen()
        if clean_pannel: self.clean_panel()
        '''
        for i in range(self.height):
            for j in range(self.width): print ("\b")
        '''
        if not cards and self.person_instance: self.normal_draw_all(self.person_instance[self.myindex].cards)
        else: self.normal_draw_all(cards)
        
        #for test
        #self.draw_play_cards(person().cards)
        
        for ind,i in enumerate(self.pannel[:self.height]): 
            #i[:2]='% 2d'%ind
            ti=''.join(i).encode('utf-8')
            ti=ti[:self.width].decode('utf-8', errors='ignore')
                        
            #len(ti.encode('utf-8'))-self.width-1
            print (ti)
            
        
    def input_withtimeout(self, informmsg='test:', func=int, timeout=Config.Timeout):
        '''
        with eventlet.Timeout(Config.Timeout,False):
            res=input(informmsg)
            if not res: return None
            try:
                res=func(res)
            except Exception as e:
                print ('input error:', str(e))
                return None
            return res
        return None
        '''
        inform=informmsg+'(%2d):'%(timeout)
        start_time = time.time()
        input = ''
        while True:
            #print ("\b"*len(inform), end='')
            print ("\r", end='')
            inform=informmsg+'(%2d):'%(timeout-time.time() + start_time)+input
            print (inform, end='')
            if msvcrt.kbhit():
                chr =  msvcrt.getche() 
                if ord(chr) == 13: break  #enter    
                elif ord(chr)==27: return None  #esc 取消                
                elif ord(chr) >= 32: #space_char
                    input += chr.decode()            
            if  (time.time() - start_time) >timeout:  return None            
        if len(input) <= 0: return self.input_withtimeout(informmsg, func, timeout=(timeout-time.time() + start_time))
        try:
            input=func(input)
        except Exception as e:
            #print ('input error:'+str(e), end='')
            return self.input_withtimeout(informmsg, func, timeout=(timeout-time.time() + start_time))
        
        return input
        
                
        
    
    def main_loop(self):
        while self.game_status :
            if not self.listen_distribute():time.sleep(0.5)
        print ('Room Destroyed!')
    
    
    def draw_panel(self, info_list, yy, xx):
        #y行x列为起点
        mlen=max([len(x.encode('utf-8')) for x in info_list])
        
        #截断
        info_list=info_list[:self.height] 
        info_list=[x[:self.width] for x in info_list]
            
        yy=min(yy, self.height-len(info_list))
        yy=max(yy, 0)
        xx=min(xx, self.width-mlen)
        xx=max(xx, 0)
        for ind,i in enumerate(info_list):
            for j in range(len(i)):
                self.pannel[yy+ind][j+xx]=i[j]        
                
    def clean_panel(self):
        for i in self.pannel:
            for j in range(len(i)):
                i[j]=' '
    
    def clean_screen(self):
        if syst == "Windows":  os.system("cls") # windows上执行cls命令
        else: os.system("clear") # linux上执行clear命令
    
    ##########################################################消息分配区
    def send_recv(self, c_sock, msg=None):
        '''
        :等待回复
        :若msg不为空则先发送msg
        '''
        if msg: Rooms.base.base.send_message_str(c_sock, msg)
        try:
            tmsg=c_sock.recv(Config.BuffSize)
            
            if not tmsg: return None
            
        except  socket.timeout:
            print ('ERROR:detected timeout')
            return None
        except Exception as e:
            print ('unexpected error:', str(e))
            return None
        msg_list_str=tmsg.decode('utf-8')
        msg_list=msg_list_str.split(Config.Message_tail)
        ret=[json.loads(x) for x in msg_list if x]
        print ('recv:',ret)
        return ret
    
    
    def listen_distribute(self, msgwant=[]):
        #return 是否执行了msg中的对应函数
        self.function_table=Message.make_msg2fun(self)
        msg_list=self.send_recv(self.socket)
        
        if not msg_list: return msg_list
        ret=False
        for ind,msg in enumerate(msg_list):
            if msgwant and msg['msg_name'] not in msgwant: continue
            
            name=msg['msg_name']
            self.function_table[name](msg)
            ret=True
        return ret
        
                
    #下面为消息响应区 ，该部分的函数应该与Messge中的一致，注意这里为收到消息的响应，其驱动为收到消息
    def str2playcard(self, pstr, cardsforsel, selcnt, endforsel):
        cards=[]
        ends=[]
        sp=pstr.split('>')
        if sp[0]:
            for  i in sp[0].split(' ,.'):
                if len(cards)<selcnt: cards.append(cardsforsel[int(i)]  )
                
        if len(sp)>1 and sp[1]:
            for  i in sp[1].split(' ,.'):
                if endforsel is None: 
                    ends.append(int(i)) 
                    continue
                if int(i) in endforsel:
                    ends.append(int(i))
        return [cards, ends]
    
    def common_msg_process(self, msg):
        self.myindex=msg['myid']
        if self.person_instance:
            for ind,i in enumerate(msg['heros']):
                if not i: continue
                #[[heroid, health],...  ]
                if self.person_instance[ind].heroid!=i[0]:
                    self.person_instance[ind]=person(i[0], ind)
                self.person_instance[ind].health=i[1]
            for ind,i in enumerate(msg['cards']):##[ [cards, armers, shields, horses_minus, horse_plus], ... ]
                if not i: continue
                self.person_instance[ind].set_all_cards(i)
    
    def on_heartbeat(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        if msg and msg['reply']:
            msg['reply']=False
            Rooms.base.base.send_map_str(self.socket, msg)
        return True        

    def on_playcard(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        st=msg['start']
        ed=msg['end']
        cards=msg['third']
        
        self.update()
        self.draw_play_cards(cards)
        
        for i in st:
            for  j in ed:
                if i!=j: self.draw_link(self.person_instance[i].playcard_y, self.person_instance[i].playcard_x,\
                                self.person_instance[j].playcard_y, self.person_instance[j].playcard_x)
        
        self.update( False)
        
        return msg
        
    
    def on_judgement(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        return False
    
    def on_getcard(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        return False
    
    def on_roundstart(self, msg=None):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        
        return False
        
    def on_roundend(self, msg=None):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        return False            
        
    def on_gamestart(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        print ('Game Start!')
        return True
    
    def on_gameend(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        print ('Game End!')
        self.game_status=False
        return True
    
    def on_skillstart(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        return False
    
    def on_equipstart(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        return False
    
    def on_inform_beforegame(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        print (msg['third'])
        return True
    
    def on_pickhero(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        hero_sel=msg['heros']
        if not hero_sel: 
            print ('select heros ERROR!')
            return False
        self.sel_hero_draw(hero_sel)
        self.update( False)
        res=self.input_withtimeout('请选择人物序号(default:0):', int)
        
        if res is None: 
            print('选择超时,使用默认')
            res=0
        heroid=hero_sel[res]
        
        if not msg['reply']: 
            print ('ERROR:while select hero')
            return
        #做个消息发回去
        msg['heros']=[heroid]
        return base.base.send_map_str(self.socket, msg)
    
    def on_gameinited(self, msg):        
        if msg['cards'] and msg['heros']: 
            for ind,i in enumerate(msg['heros']):
                self.person_instance.append( person(i[0], ind) )
                
            self.common_msg_process(msg)
        self.update()
        return True
    
    def on_roundend_dropcard(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        '''
        dropedcards=[self.cards[x]  for x in msg['third']]
        self.cards=[self.cards[x]  for x in range(len(self.cards)) if (x not in msg['third'])]
        self.room.drop_cards(dropedcards)
        '''
        return True
        
    
    def on_askselect(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        #返回的msg中third中为用户选择，forth为选择的card，
        #return False
        
        if self.myindex not in msg['start']: 
            print ("\r%s Selecting..."%Persons.class_list[msg['start'][0]].name, end='')
            return
        
        
        self.update(msg['forth'])
        
        res=self.input_withtimeout(msg['third'], str)
        if res is None: 
            msg['third']=False
            Rooms.base.base.send_map_str(self.socket, msg)
            return False
        #或者是出牌
        cards,ends=self.str2playcard(res, msg['forth'], msg['fifth'], msg['end'])
        msg_p=Message.form_playcard(self.myindex, msg['heros'], msg['cards'], [self.myindex], ends, cards, reply=False)  #通知所有人谁向谁出了牌
        Rooms.base.base.send_map_str(self.socket, msg_p)
        
        return True
    
    
    
    ####################################################网络部分
    def connect_server(self, ipstr='127.0.0.1'):
        # 创建 socket 对象
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
            #s.settimeout(Config.Timeout)
            # 连接服务，指定主机和端口
            s.connect((ipstr, Config.Port))
            
            #s.settimeout(None)
        except  socket.timeout:
            print ('ERROR:detected timeout server not online')
            return None
        except Exception as e:
            print ('unexpected error:',str(e))
            return None
        
        return s
    
    
    
    
if __name__=="__main__":
    ipstr=input('请输入服务器IP(default:127.0.0.1)：')
    if not ipstr: ipstr='127.0.0.1'
    tep=UI_cmd(ipstr)
    
    tep.main_loop()
    
    
    
    
    
    
    
    
    
    
        