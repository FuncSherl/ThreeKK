'''
Created on 2020年2月27日

@author: sherl
'''
import Cards,Persons
from Common import Config,Message

import platform
syst = platform.system()

class person(object):
    '''
    classdocs
    '''
    mheight=8

    def __init__(self, id=0):
        '''
        :#这里的id为英雄的标识id
        '''
        self.heroid=id
        self.name=Persons.class_list[id].name_pinyin
        self.health=Persons.class_list[id].blood
        self.describ_hero=Persons.class_list[id].describ_skill_list
        self.cards=[]
        self.armers=[]
        self.shields=[]
        self.horse_minus=[]
        self.horse_plus=[]
        self.mlen=0
        self.mydescr=self.get_describe()
        self.mhigh=len(self.mydescr)
        self.alive=True
        
    def set_all_cards(self, all_the_cards_holders):
        self.cards, self.armer, self.shield, self.horse_minus, self.horse_plus=all_the_cards_holders
        
    
    def add_box(self, info_list):
        mlen=max([len(x.encode('utf-8')) for x in info_list])+2
        self.mlen=mlen
        for i in range(len(info_list)):
            info_list[i]='|'+info_list[i]+' '*(mlen-2-len(info_list[i].encode('utf-8')))+'|'
        
        info_list.insert(0, '-'*mlen)
        info_list.append('-'*mlen)
        return info_list
    
    def get_hero_describe(self):
        ret= ['HERO:'+self.name+'  ' +'H'*self.health]
        mlen=max([len(x.encode('utf-8')) for x in ret])
        mlen=int(mlen/2)  #中文与英文显示对应
        mlen=max(mlen, 12)
        
        for i in self.describ_hero:
            if not i : continue
            st=0
            while st<len(i):
                ret.append(i[st: st+mlen])
                st+=mlen
        return self.add_box(ret)
                
    def to_red(self, str):
        return '\033[1;35;0m'+str+' \033[0m'
    
    def form_other_person(self):
        return ['HERO:'+self.name+'  H:' +'*'*self.health, 'ARMERS:'+','.join( [Cards.class_list[x[0]].name_pinyin for x in self.armers]),\
              'SHIELDS:'+','.join( [Cards.class_list[x[0]].name_pinyin for x in self.shields]), \
              'HORSE+1:'+','.join( [Cards.class_list[x[0]].name_pinyin for x in self.horse_plus]),\
              'HORSE-1:'+','.join( [Cards.class_list[x[0]].name_pinyin for x in self.horse_minus]),  'CARDS:'+'N'*len(self.cards)]
        
    def get_describe(self):
        return self.add_box(self.form_other_person())
        
    @classmethod
    def form_card(cls, card):
        name=Cards.class_list[card[0]].name_pinyin
        #\033[显示方式;前景色;背景色m + 结尾部分：\033[0m
        lmin=min([len(x) for x in Config.Card_color_enum])
        col=Config.Card_color_enum[card[1]].upper()
        return '['+name+':'+col+':'+'%d'%(card[2])+']'
        
    def form_all_cards(self):
        return [self.form_card(x) for x in self.cards]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        