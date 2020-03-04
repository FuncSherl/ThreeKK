#coding:utf-8
'''
Created on 2020年2月26日

@author: sherl
'''
import os,sys
sys.path.append(os.path.abspath('.'))

import math,re
import Cards,Persons,Rooms
from Rooms import base
from Common import Config,Message
from UI_Cmd.person import person 
import socket ,time
import json,select
import numpy as np
import platform
syst = platform.system()

if syst=='Windows':      import msvcrt

#import eventlet
#eventlet.monkey_patch()


class UI_cmd:        
    height=30-1  #cmd为30行
    width=120-2 #120列个字符
    

    user_stx=int(width/4)
    user_sty=int(height*1/2)
    
    playarea_y=person.mheight+10
    
    center_x=int(width/2)
    center_y=int(  (center_x**2 + user_sty**2)/ (2*user_sty)   )
    start_angle=math.acos(center_x*1.0/center_y)
    
    split_card_hero='>'
    split_cards=r'\s*[;,\.\s]\s*'
    split_heros=split_cards
    
    def __init__(self, ipstr='127.0.0.1'):
        self.ipstr=ipstr
        self.socket=None
        while not self.socket: self.socket=self.connect_server(self.ipstr)
        
        self.msg_queue=[]
        self.listen_fail_cnt=0

        self.pannel=[]
        for i in range(self.height):
            self.pannel.append([])
            for j in range(self.width):
                self.pannel[-1].append(ord(' '))
        #最多支持6个人才不会重叠
        self.person_instance=[]#[person(0,0), person(1,1),person(2,2),person(1,1),person(2,2)]
        self.myindex=0
        self.game_status=True
        #self.pannel[:,:]=ord(' ')
        #char->ascll ord('c')
        #ascll->char chr(97)
        #for i in self.pannel: print (''.join(i))
        self.played_cards=[[], [], []]   #[[cards],[sts],[ends]  ]
        self.update()
        
        
        
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
            
            self.person_instance[st].playcard_x=int( self.width/2-(self.width/2-tx)/3 )
            self.person_instance[st].playcard_y=int( ty+len(descrs[st])+1  ) 
            
            st=(st-1)%len(self.person_instance)
        
            
        
    def draw_me(self):
        if not self.person_instance:return
        desr=self.person_instance[self.myindex].get_describe()
        self.draw_panel(desr, self.height, self.width) #放到右下角，自动识别更改
        
    def draw_my_cards(self):
        if not self.person_instance:return
        res=self.person_instance[self.myindex].form_all_cards()
        mlen=self.person_instance[self.myindex].mlen
        mhight=self.person_instance[self.myindex].mhigh
        stx=0
        sty=self.height-mhight-1
        
        self.draw_panel(['*'*self.width], sty, stx)        
        sty+=2
        
        for ind,i in enumerate(res):
            tstr=str(ind)+'>'+i+'    '
            if stx+person.get_show_len(tstr)+mlen+1>self.width:
                stx=0
                sty+=2
            _,stx=self.draw_panel([tstr], sty, stx)
            #print (self.pannel[sty])
            
    def draw_play_cards(self):
        #played_cards[[cards],[sts],[ends]  ]
        descs=[person.form_card(x) for x in self.played_cards[0]]
        if not descs: return
        mlen=max( [len(x) for x in descs] )
        stx=int((self.width-mlen)/2)
        self.draw_panel(descs, self.playarea_y-len(self.played_cards[0]), stx)
        
        self.person_instance[self.myindex].playcard_x=int( self.width/2)
        self.person_instance[self.myindex].playcard_y=self.playarea_y-len(self.played_cards[0])-1
        
        for i in self.played_cards[1]:
            for j in self.played_cards[2]:
                self.draw_link(self.person_instance[i].playcard_y, self.person_instance[i].playcard_x, self.person_instance[j].playcard_y, self.person_instance[j].playcard_x)
                
        
    def draw_link(self, sty, stx, edy, edx):
        kep_stx=stx
        kep_sty=sty
        inch_x=1 if edx>stx else -1
        inch_y=1 if edy>sty else -1
        while not (stx==edx and sty==edy):
            #print (stx,sty, edx, edy)
            if abs(edy-sty)>abs(edx-stx):
                self.panel_set_at('|', stx, sty)
                #self.pannel[sty][stx]=ord(b'|')
                sty+=inch_y
            elif abs(edy-sty)<abs(edx-stx):
                self.panel_set_at('-', stx, sty)
                #self.pannel[sty][stx]=ord(b'-')
                stx+=inch_x
            else:
                self.panel_set_at('/', stx, sty)
                #self.pannel[sty][stx]=ord(b'/')
                if (edy-sty)*(edx-stx)>=0: 
                    self.panel_set_at('\\', stx, sty)
                    #self.pannel[sty][stx]=ord(b'\\')
                stx+=inch_x
                sty+=inch_y
        tep=None
        if abs(edy-kep_sty)>abs(edx-kep_stx): 
            tep='^'
            if edy>kep_sty:tep='v'
        else:
            tep='<'
            if edx>kep_stx: tep='>'
        self.panel_set_at(tep, stx, sty)
        #self.pannel[sty][stx]=(tep)
            
    def normal_draw_all(self, cards_list):
        #正常对局下的每次打印
        self.draw_clients()
        self.draw_me()
        self.draw_my_cards()
        
    def sel_hero_draw(self, heroidlist):
        desc_list=[person(y, 0).get_hero_describe() for y in heroidlist]
        mlist=[ max([person.get_show_len(x) for x in y])  for y in desc_list]
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

        if not cards and self.person_instance: self.normal_draw_all(self.person_instance[self.myindex].cards)
        else: self.normal_draw_all(cards)
        
        #for test
        self.draw_play_cards()
        
        for ind,i in enumerate(self.pannel): 
            #i[:2]='% 2d'%ind
            ti=''.join(i)
            #ti=ti[:self.width].decode('utf-8', errors='ignore')
            #print ( i)
            #ti=bytes(i).decode( errors='ignore')
                        
            #len(ti.encode('utf-8'))-self.width-1
            print (ti)
            
        
    def input_withtimeout(self, informmsg='test:', func=int, timeout=Config.Select_Timeout, default=None):
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
        if syst == "Windows":  return self.input_withtimeout_windows(informmsg, func, timeout, default)
        else: 
            return self.input_withtimeout_linux(informmsg, func, timeout, default)
        
    def input_withtimeout_linux(self, informmsg='test:', func=int, timeout=Config.Select_Timeout, default=None):
        def str2width(str):
            str_b=str.encode()
            l_m=len(str_b)-len(str)
            return str.ljust(self.width-l_m)
        
        #清空输入缓冲
        have_char=True
        while have_char:
            r, w, x = select.select([sys.stdin], [], [], 0.0)
            have_char = (r and r[0] == sys.stdin)
            if have_char: sys.stdin.read(1)
        
        inform=str2width(informmsg+'(%2d):'%(timeout))
        start_time = time.time()
        input_str = ''
        while True:
            #print ("\b"*len(inform), end='')
            print ("\r", end='')
            inform=str2width(informmsg+'(%2d):'%(timeout-time.time() + start_time)+input_str)
            print (inform, end='')
            
            r, w, x = select.select([sys.stdin], [], [], 0.0)
            have_char = (r and r[0] == sys.stdin)
            
            if have_char:
                chr =  sys.stdin.read(1) 
                #print (ord(chr))
                if ord(chr) == 13: break  #enter    
                elif ord(chr)==27: return default  #esc 取消        
                elif ord(chr)== 8: input_str=input_str[:-1]      #backspace  
                elif ord(chr) >= 32: #space_char
                    input_str += chr.decode()            
            if  (time.time() - start_time) >timeout:  return default            
        
        if len(input_str) <= 0: return default
            
        try:
            input_str=func(input_str)
        except Exception as e:
            #print ('input error:'+str(e), end='')
            return default
        
        return input_str
        
        
    def input_withtimeout_windows(self, informmsg='test:', func=int, timeout=Config.Select_Timeout, default=None):        
        def str2width(str):
            str_b=str.encode()
            l_m=len(str_b)-len(str)
            return str.ljust(self.width-l_m)
        
        #sys.stdin.flush()#清空输入缓冲
        while msvcrt.kbhit():msvcrt.getche()
        
        inform=str2width(informmsg+'(%2d):'%(timeout))
        start_time = time.time()
        input_str = ''
        while True:
            #print ("\b"*len(inform), end='')
            print ("\r", end='')
            inform=str2width(informmsg+'(%2d):'%(timeout-time.time() + start_time)+input_str)
            print (inform, end='')
            if msvcrt.kbhit():
                chr =  msvcrt.getche() 
                #print (ord(chr))
                if ord(chr) == 13: break  #enter    
                elif ord(chr)==27: return default  #esc 取消        
                elif ord(chr)== 8: input_str=input_str[:-1]      #backspace  
                elif ord(chr) >= 32: #space_char
                    input_str += chr.decode()            
            if  (time.time() - start_time) >timeout:  return default            
        
        if len(input_str) <= 0: return default
            
        try:
            input_str=func(input_str)
        except Exception as e:
            #print ('input error:'+str(e), end='')
            return default
        
        return input_str
        
                
        
    
    def main_loop(self):
        while self.game_status :
            if not self.listen_distribute():
                self.listen_fail_cnt+=1
                if self.listen_fail_cnt>Config.FailerCnt: 
                    self.game_status=False
                time.sleep(0.5)
            else: self.listen_fail_cnt=0
        print ('Room Destroyed!')
    
    def panel_set_at(self, char_str, stx, sty):
        if sty>=len(self.pannel): return stx     #self.panel_set_at(char_str, 0, 0)
        if stx>=len(self.pannel[0]):  return stx     #self.panel_set_at(char_str, 0, sty+1)
        self.pannel[sty][stx]=char_str        
        if len(char_str.encode())>1:            
            self.pannel[sty][stx+1]=''
            return stx+2
        return stx+1
            
    
    
    def draw_panel(self, info_list, yy, xx):
        #info_list=[ x.encode() for x in info_list]
        #y行x列为起点
        mlen=max([person.get_show_len( x) for x in info_list])
        
        #截断
        info_list=info_list[:self.height] 
        for i in info_list:
            while person.get_show_len( i )>self.width: i=i[:-1]
            
        yy=min(yy, self.height-len(info_list))
        yy=max(yy, 0)
        xx=min(xx, self.width-mlen)
        xx=max(xx, 0)
        for ind,i in enumerate(info_list):
            stxx=xx
            styy=yy+ind
            for j in range(len(i)):
                stxx=self.panel_set_at(i[j], stxx, styy)
                #self.pannel[yy+ind][j+xx]=i[j]    
        return     styy, stxx
                
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
            print ('recv:',tmsg)  #DEBUG
        except  socket.timeout:
            print ("\rERROR:detected timeout", end='')
            return None
        except Exception as e:
            print ("\runexpected error:"+ str(e), end='')
            return None
        msg_list_str=tmsg.decode('utf-8')
        #print ('recv:',msg_list_str)
        msg_list=msg_list_str.split(Config.Message_tail)
        ret=[json.loads(x) for x in msg_list if x]
        #print ('recv:',ret)
        return ret
    
    
    def listen_distribute(self, msgwant=[]):
        self.function_table=Message.make_msg2fun(self)
        
        while self.msg_queue:
            #print (self.msg_queue)
            name=self.msg_queue[0]['msg_name']
            if msgwant and name not in msgwant: self.msg_queue.pop(0)
            else: return self.function_table[name](self.msg_queue.pop(0))
        
        msg_list=self.send_recv(self.socket)
        
        if not msg_list: return msg_list
        
        self.msg_queue.extend(msg_list)

        return self.listen_distribute(msgwant)
        
                
    #下面为消息响应区 ，该部分的函数应该与Messge中的一致，注意这里为收到消息的响应，其驱动为收到消息
    def str2playcard(self, pstr,  selcnt, endforsel=[]):
        #selcnt选几张牌  endforsel：可选的end
        
        cards=[]
        ends=[]
        try:
            sp=re.split(self.split_card_hero, pstr)
            print (sp)#DEBUG  ['1,2']
            if sp[0]:
                for  i in re.split(self.split_cards, sp[0]):
                    print ('cards :',cards)
                    if len(cards)<selcnt and int(i)<len(self.person_instance[self.myindex].cards) and int(i)>=0: 
                        cards.append(self.person_instance[self.myindex].cards[int(i)]  )
                    
            if len(sp)>1 and sp[1]:
                for  i in re.split(self.split_heros, sp[1]):
                    if not i : continue
                    
                    if endforsel is None and int(i)<len(self.person_instance) and int(i)>=0: 
                        ends.append(int(i)) 
                        continue
                    if int(i) in endforsel:
                        ends.append(int(i))
        except Exception as e:
            print ("str2playcard error:"+str(e), end='')
            #str2playcard error:invalid literal for int() with base 10: '1,2'
        finally:
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
            for ind,i in enumerate(msg['cards']):##[ [cards, armers, shields, horses_minus, horse_plus, delayedskill], ... ]
                if not i: continue
                self.person_instance[ind].set_all_cards(i)
        self.update(clean_pannel=True)
    
    def on_heartbeat(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        if msg and msg['reply']:
            msg['reply']=False
            
        return   Rooms.base.base.send_map_str(self.socket, msg)

    def on_playcard(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        st=msg['start']
        ed=msg['end']
        cards=msg['third']

        #self.draw_play_cards()
        self.played_cards=[cards, st, ed]
        
        for i in st:
            for  j in ed:
                print ("\r%s对%s使用了:%s"%(  (self.person_instance[i].name if i!=self.myindex else '你'), (self.person_instance[j].name if j!=self.myindex else '你'),\
                                        ','.join([Cards.class_list[x[0]].name for x in cards  ])  ), end='')
                
                if i!=j: self.draw_link(self.person_instance[i].playcard_y, self.person_instance[i].playcard_x,\
                                self.person_instance[j].playcard_y, self.person_instance[j].playcard_x)
        
        self.update( )
        
        #print (self.pannel)  #DEBUG
        #self.played_cards=[[],[],[]]
        
        return msg
        
    
    def on_judgement(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        return True
    
    def on_getcard(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        st=msg['start']
        ed=msg['end']
        cards=msg['third']
        cards=[] if not cards else cards
        
        for j in ed:
            print ("\r%s从%s摸了%d张牌.."%(  (self.person_instance[j].name if j!=self.myindex else '你'), \
                                        ('牌堆中' if not st else ('你' if st[0]==self.myindex else self.person_instance[st[0]].name)),\
                                        len(cards)  ), end='')
        
        return True
    
    def on_roundstart(self, msg=None):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        print ("\r%s回合开始..."% self.person_instance[msg['start']].name , end='')
        return True
        
    def on_roundend(self, msg=None):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        print ("\r本回合结束...", end='')
        return True            
        
    def on_gamestart(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        print ("\rGame Start!", end='')
        return True
    
    def on_gameend(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        print ("\rGame End!", end='')
        self.game_status=False
        return True
    
    def on_skillstart(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        return True
    
    def on_equipstart(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        return True
    
    def on_inform_beforegame(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        print ("\r"+msg['third'], end='')
        return True
    
    def on_pickhero(self, msg):
        #if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        
        hero_sel=msg['heros']
        if not hero_sel: 
            print ("Select Heros ERROR!", end='')
            return False
        self.sel_hero_draw(hero_sel)
        self.update( False)
        res=self.input_withtimeout('请选择人物序号(default:0):', int,default=0)
        
        if res is None: 
            print("\r选择超时,使用默认", end='')
            res=0
        heroid=hero_sel[res]
        
        if not msg['reply']: 
            print ("\rERROR:while select hero", end='')
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
        st=msg['start'][0]
        dcnt=msg['third'][0]
        
        if st!=self.myindex: 
            print ("\r%s Droping %2d Cards..."%(self.person_instance[st].name, dcnt), end='')
            return True        
        res=self.input_withtimeout('回合结束，请弃%d张牌:'%dcnt, str)
        
        
        
        if not res:
            msg=Message.form_askselect(self.myindex, msg['heros'], msg['cards'], [self.myindex], None, None, [], select_cnt=0, reply=False)
            return Rooms.base.base.send_map_str(self.socket, msg)
        
        cards,ends=self.str2playcard(res, dcnt)
        
        msg['start']=[self.myindex]
        msg['end']=None
        msg['third']=cards
        msg['reply']=False        
        
        return Rooms.base.base.send_map_str(self.socket, msg)
        
    
    def on_askselect(self, msg):
        if msg['cards'] and msg['heros']: self.common_msg_process(msg)
        #返回的msg中third中为用户选择，forth为选择的card，
        #return False
        
        if self.myindex not in msg['start']: 
            print ("\r%s Selecting..."%self.person_instance[msg['start'][0]].name, end='')
            return True
        
        self.person_instance[self.myindex].cards_to_sel=msg['forth']
        self.update()
        
        res=self.input_withtimeout(msg['third'], str)
        if res is None: 
            self.person_instance[self.myindex].cards_to_sel=[]
            msg['third']=False
            return Rooms.base.base.send_map_str(self.socket, msg)
            
        #或者是出牌
        cards,ends=self.str2playcard(res, msg['fifth'], msg['end'])
        msg_p=Message.form_playcard(self.myindex, msg['heros'], msg['cards'], [self.myindex], ends, cards, reply=False)  #通知所有人谁向谁出了牌
        
        self.person_instance[self.myindex].cards_to_sel=[]
        return Rooms.base.base.send_map_str(self.socket, msg_p)
    
    
    
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
    
    
    
    
    
    
    
    
    
    
        