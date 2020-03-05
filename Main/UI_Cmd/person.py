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

    def __init__(self, id, myindex):
        '''
        :#这里的id为英雄的标识id
        '''
        self.heroid=id
        self.myindex=myindex
        self.name=Persons.class_list[id].name
        self.name_chinese=Persons.class_list[id].name
        self.health=Persons.class_list[id].blood
        self.describ_hero=Persons.class_list[id].describ_skill_list
        self.cards=[]#[[2,1,2], [1,2,3], [3,3,6], [4, 2, 12]]
        self.cards_to_sel=[]
        self.armers=[]
        self.shields=[]
        self.horse_minus=[]
        self.horse_plus=[]
        self.delayed_skill=[]
        
        self.mlen=0
        self.mydescr=self.get_describe()
        self.mhigh=len(self.mydescr)
        self.alive=True
        self.playcard_x=0
        self.playcard_y=0
        
    def set_all_cards(self, all_the_cards_holders):
        self.cards, self.armers, self.shields, self.horse_minus, self.horse_plus, self.delayed_skill=all_the_cards_holders
        
    
    def add_box(self, info_list, withleft=True, withright=True):
        showlens=[self.get_show_len(x) for x in info_list]
        #print (showlens)
        mlen=max(showlens)+int(withright)+int(withleft)
        self.mlen=mlen
        for i in range(len(info_list)):
            info_list[i]=''.join( [  ('|' if withleft else '')  ,info_list[i], \
                                   (' ' if withright else '')*(mlen-int(withright)-int(withleft)-self.get_show_len(info_list[i])), \
                                   '|' if withright else ''] )
            #info_list[i]=info_list[i].encode()[:mlen].decode( errors='ignore')
        
        info_list.insert(0, '-'*mlen)
        info_list.append('-'*mlen)
        #print (info_list)
        return info_list
    
    def get_hero_describe(self):
        ret= ['人物:'+self.name_chinese+'  血量:' +'*'*self.health]
        mlen=max([self.get_show_len(x) for x in ret])
        #mlen=int(mlen/2)  #中文与英文显示对应
        
        for i in self.describ_hero:
            if not i : continue
            ret.append(i)            
        return self.add_box(ret, True, True)
                
    def to_red(self, str):
        return '\033[1;35;0m'+str+' \033[0m'
    
    @classmethod
    def get_show_len(cls, strl):
        #utf-8一个中文占用3字节，显示占用2字节
        return int (len(strl)+ (len(strl.encode())-len(strl))/2  )
    
    def form_other_person(self):
        return ['INDEX:%d'%self.myindex,\
                '人物:'+self.name_chinese+'  HP:' +'*'*self.health, \
                '武器:'+','.join( [Cards.class_list[x[0]].name for x in self.armers]),\
              '防御:'+','.join( [Cards.class_list[x[0]].name for x in self.shields]), \
              '马+1:'+','.join( [Cards.class_list[x[0]].name for x in self.horse_plus]),\
              '马-1:'+','.join( [Cards.class_list[x[0]].name for x in self.horse_minus]),  '手牌:'+'N'*len(self.cards),\
              '状态:'+','.join( [Cards.class_list[x[0]].name for x in self.delayed_skill])]
        
    def get_describe(self):
        return self.add_box(self.form_other_person())
        
    @classmethod
    def form_card(cls, card, cards_to_sel=[], withdesc=False):
        name=Cards.class_list[card[0]].name
        #\033[显示方式;前景色;背景色m + 结尾部分：\033[0m
        lmin=min([len(x) for x in Config.Card_color_enum])
        col=Config.Card_color_chinese[card[1]].upper()
        return '['+name+':'+col+':'+'%d'%(card[2])+']'+('*' if card in cards_to_sel else '') \
            + (':'+Cards.class_list[card[0]].describe if withdesc else '')
    
    
    def form_all_cards(self):
        for i in self.cards_to_sel: 
            if i not in self.cards: self.cards.append(i)
        return [self.form_card(x, self.cards_to_sel) for x in self.cards]
        
        
        
        
if __name__ == '__main__':
    stt='str'
    print (len(stt))
    print (len(stt.encode()))
    print (person.get_show_len(stt))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        