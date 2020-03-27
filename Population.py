import random
import math
import collections
import matplotlib.pyplot as plt
from Person import Person


class Population:
    def __init__(self,m,f,years=100):
        # 0 is male, 1 es female
        self.men=[Person(0) for _ in range(m)]
        self.women=[Person(1) for _ in range(f)]
        self.time=years*12
        # couples to break
        self.couples=[]
        # number of couples
        self.noc=0
        # kids to be born
        self.kids=collections.deque()
        # number of birth per year
        self.nobpy=0
        # list of number of birth per year
        self.lnobpy=[]
         # number of death per year
        self.nodpy=0
        # list of number of death per year
        self.lnodpy=[]  
        # list of number of men per year
        self.nom=[]
        # list of number of men per year
        self.now=[]

    def remove_dead_people(self):
        i=0
        while(i<len(self.men)):
            if self.men[i].is_dead():
                self.men.remove(self.men[i])
                self.nodpy+=1
            else:
                i+=1   
        i=0
        while(i<len(self.women)):
            if self.women[i].is_dead():
                self.women.remove(self.women[i])
                self.nodpy+=1
            else:
                i+=1 

    def run(self):
        self.remove_dead_people()
        count=0
        while self.time!=0:
            if count%12==0:
                self.store_data()
            for i in self.men:
                i.one_more_month()
            for i in self.women:
                i.one_more_month()
            self.remove_dead_people()
            for i in self.couples:
                i[2]-=1
            for i in self.kids:
                i[0]-=1
            self.give_birth()
            self.make_kids()
            self.remove_couples()
            self.make_couples()
            count+=1
            self.time-=1

    def remove_couples(self):
        i=0
        while(i<len(self.couples)):
            if self.couples[i][2]==0:
                self.couples[i][0].single=True
                self.couples[i][1].single=True
                self.couples[i][0].set_mourning_time()
                self.couples[i][1].set_mourning_time()
                self.couples.remove(self.couples[i])
                self.noc-=1
            else:
                i+=1 
    def add_couple(self, am,aw,per):
        p=random.random()
        if p<per:
            self.noc+=1
            pb=random.random()
            t1=am.death_time-am.age
            t2=aw.death_time-aw.age
            if pb<0.2:
                t3=random.randint(1,max(min(t1,t2)-1,1))
                self.couples.append([am,aw,t3,0])
            else:
                self.couples.append([am,aw,min(t1,t2),0])
            aw.single=False
            am.single=False
            return True
        return False   

    def make_couples(self):
        for aw in [w for w in self.women if w.single and w.mourning==0 and w.wtbiac]:
            for am in self.men:
                if am.single and am.mourning==0 and am.wtbiac:
                    leap=int(abs(aw.age-am.age)/12)
                    if leap<5:
                        if self.add_couple(am,aw,0.45):
                            break
                        else:
                            continue
                    if leap<10:
                        if self.add_couple(am,aw,0.4):
                            break
                        else:
                            continue
                    if leap<15:
                        if self.add_couple(am,aw,0.35):
                            break
                        else:
                            continue
                    if leap<20:
                        if self.add_couple(am,aw,0.25):
                            break
                        else:
                            continue
                    self.add_couple(am,aw,0.15)

    def number_of_kids(self):
        table=[0.68,0.86,0.94,0.98,1]
        ct=random.random()
        for i in range(len(table)):
            if ct<table[i]:
                return i+1 

    def make_kids(self):
        
        for cp in self.couples:
            if  (cp[0].want_kid() or cp[1].want_kid()) and cp[1].birth_time==0:
                p=random.random()
                if 12*12<=cp[1].age and cp[1].age<15*12 and cp[1].death_time-cp[1].age>9:
                    if p<0.2:
                        cp[1].birth_time=9
                        cp[0].number_of_kids+=1
                        cp[1].number_of_kids+=1
                        self.kids.append([9,self.number_of_kids()])
                    continue
                if  cp[1].age<21*12 and cp[1].death_time-cp[1].age>9:
                    if p<0.45:
                        cp[1].birth_time=9
                        cp[0].number_of_kids+=1
                        cp[1].number_of_kids+=1
                        self.kids.append([9,self.number_of_kids()])
                    continue
                if cp[1].age<35*12 and cp[1].death_time-cp[1].age>9:
                    if p<0.8:
                        cp[1].birth_time=9
                        cp[0].number_of_kids+=1
                        cp[1].number_of_kids+=1
                        self.kids.append([9,self.number_of_kids()])
                        continue
                if cp[1].age<45*12 and cp[1].death_time-cp[1].age>9:
                    if p<0.4:
                        cp[1].birth_time=9
                        cp[0].number_of_kids+=1
                        cp[1].number_of_kids+=1
                        self.kids.append([9,self.number_of_kids()])
                    continue                
                if cp[1].age<60*12 and cp[1].death_time-cp[1].age>9:
                    if p<0.2:
                        cp[1].birth_time=9
                        cp[0].number_of_kids+=1
                        cp[1].number_of_kids+=1
                        self.kids.append([9,self.number_of_kids()])
                    continue    
                if  cp[1].age<125*12 and cp[1].death_time-cp[1].age>9:
                    if p<0.05:
                        cp[1].birth_time=9
                        cp[0].number_of_kids+=1
                        cp[1].number_of_kids+=1
                        self.kids.append([9,self.number_of_kids()])
    def give_birth(self):
        ac=0
        while len(self.kids)!=0 and self.kids[0][0]==0:
            ac+=self.kids[0][1]
            self.kids.popleft()
        news=[Person(age=0) for _ in range(ac) ]
        self.men.extend([x for x in news if x.sex==0])
        self.women.extend([x for x in news if x.sex==1])
        self.nobpy+=ac
    def store_data(self):
        self.lnobpy.append(self.nobpy)
        self.nobpy=0
        self.lnodpy.append(self.nodpy)
        self.nodpy=0
        self.nom.append(len(self.men))
        self.now.append(len(self.women))
    def showdata(self):
        x=[i for i in range(len(self.lnobpy))]
        plt.figure()
        plt.subplot(211)
        plt.plot(x,self.lnobpy,x,self.lnodpy)
        plt.xlabel("Years")
        plt.ylabel("People")
        plt.legend(["Births","Deaths"])
        plt.subplot(212)
        plt.plot(x,[self.now[i]+self.nom[i] for i in range(len(self.lnobpy))],x,self.nom,x,self.now)
        plt.ylabel("People")
        plt.xlabel("Years")
        plt.legend(["Total","Men","Women"])
        plt.show()
        



