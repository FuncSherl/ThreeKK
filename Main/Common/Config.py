#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
Port=7999   #监听端口
Timeout=18   #recv的超时时间 s
HeartBeat=3 #心跳时间间隔 s 
FailerCnt=5
BuffSize=1024*2   #recv bufsize
HerosforSelect=3    #提供多少person供选择
Cardsforinit=4  #一开始每个人多少牌
Cardeachround=2 #默认每回合起多少牌

Card_color_enum=['spade', 'club','heart', 'diamond'] #黑桃、梅花、红心、方片
Card_color_chinese=['黑桃' , '梅花', '红心', '方片']
Card_type_enum=['basic', 'skill', 'armer', 'shield', 'horse_minus', 'horse_plus']
Card_num_max=13
Card_num_min=1

All_people_cnt=20   #当向所有人出牌时，目标数目

Message_tail='#*#'