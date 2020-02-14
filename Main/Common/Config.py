#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
Port=7999   #监听端口
Timeout=8   #recv的超时时间 s
HeartBeat=3 #心跳时间间隔 s 
BuffSize=1024*8   #recv bufsize
HerosforSelect=1    #提供多少person供选择
Cardsforinit=4  #一开始每个人多少牌
Cardeachround=2 #默认每回合起多少牌

Card_color_enum=['spade', 'club','heart', 'diamond'] #黑桃、梅花、红心、方片
Card_num_max=13
Card_num_min=1
