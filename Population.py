import random
import math
import collections
import matplotlib.pyplot as plt


def roud_well(n):
    if n-math.floor(n)<0.5:
        return math.floor(n)
    return math.ceil(n)

class Person:
    def __init__(self,sex=None,age=None):
        # 0 is male, 1 es female
        self.sex= sex if not sex is None else (0 if random.random()<0.5 else 1)
        # age is in months
        self.age=age if not age is None else random.randint(0,100*12)
        self.death_time= self.cal_death_time(self.age,self.sex)
        # want to be in a couple
        self.wtbiac=self.c_wtbiac(self.age)
        self.number_of_kids_wanted=0
        self.number_of_kids=0
        # is the person single
        self.single=True
        # time to wait after breking up
        self.mourning=0
        #time left to give birth
        self.birth_time=0
        while self.one_more_kid():
            pass
        
    def one_more_kid(self):
        prob=[0.6,0.75,0.35,0.2,0.1]
        if self.number_of_kids_wanted<5:
            if random.random()<prob[self.number_of_kids_wanted]:
                self.number_of_kids_wanted+=1
                return True
        else:
             if random.random()<0.05:
                self.number_of_kids_wanted+=1
                return True
        return False

    @staticmethod
    def c_wtbiac(age):
        a=random.random()
        if age<12*12:
            return 0
        if 12*12<=age and age<15*12:
            return a<0.6
        if 15*12<=age and age<12*21:
            return a<0.65
        if 21*12<=age and age<35*12:
            return a<0.8
        if 35*12<=age and age<45*12:
            return a<0.6
        if 45*12<=age and age<60*12:
            return a<0.5
        if 65*12<=age and age<=125*12:
            return a<0.2
        
    def is_dead(self):
        return self.death_time==self.age
    # if you want another kid 
    def want_kid(self):
        return self.number_of_kids<self.number_of_kids_wanted
    @staticmethod
    def cal_death_time(age,sex):
        prob=[0]*5
        prob[4]=1
        table=[0,12,45,76,125,125]

        if age<125*12:
            prob[3]= 0.7 if sex ==0 else 0.65
        if age<76*12:
            prob[2]= 0.3 if sex ==0 else 0.35
        if age<45*12:
            prob[1]= 0.1 if sex ==0 else 0.15
        if age<12*12:
            prob[0]= 0.25 if sex ==0 else 0.25
        
        for i in range(5):
            a= random.random()
            if a<prob[i]:
                period=i+1
                break

        return random.randint(max(age+1,table[period-1]*12),table[period]*12)

    def set_mourning_time(self):
        t= random.random()
        l=0
        if 12*12<=self.age and self.age<15*12:
            l=1/3
        elif self.age<35*12:
            l=1/6
        elif self.age<45*12:
            l=1/12
        elif self.age<60*12:
            l=1/24
        else:
            l=1/48
        self.mourning=roud_well(math.log(t,math.e)/-l)
        
    def one_more_month(self):
        self.age+=1
        if self.age==12*12 or self.age==15*12 or self.age==21*12 or self.age==35*12 or self.age==45*12 or self.age==60*12:
            self.wtbiac=self.c_wtbiac(self.age)
        self.mourning= max(0 ,self.mourning-1)
        self.birth_time= max(0 ,self.birth_time-1)

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
        plt.subplot(311)
        plt.plot(x,self.lnobpy)
        
        plt.subplot(312)
        plt.plot(x,self.lnodpy)
        
        plt.subplot(313)
        plt.plot(x,[self.now[i]+self.nom[i] for i in range(len(self.lnobpy))])
        plt.show()
        

a=Population(500,500,100)
a.run()
a.showdata()

