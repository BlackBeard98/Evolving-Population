import random
import math


def roud_well(n):
    if n-math.floor(n)<0.5:
        return math.floor(n)
    return math.ceil(n)
s=0
d=0
for _ in range(100):
    t= random.random()
    k=math.log(t,math.e)/(-1/3)
    s+= roud_well(k)
    d+=k

class Person:
    def __init__(self,sex=None):
        # 0 is male, 1 es female
        self.sex= sex if not sex is None else (0 if random.random()<0.5 else 1)
        # age is in months
        self.age= random.randint(0,100*12)
        self.death_time= self.cal_death_time(self.age,self.sex)
        # want to be in a couple
        self.wtbiac=self.c_wtbiac(self.age)
        # one more kid?
        self.omk=True
        # number of kids
        self.number_of_kids=0
        # is the person single
        self.single=True
        # time to wait after breking up
        self.mourning=0
        
    def one_more_kid(self):
        if self.omk == False:
            return False
        prob=[0.6,0.75,0.35,0.2,0.1]
        if random.random()<prob[self.number_of_kids]:
            self.number_of_kids+=1
            return True
        self.omk=False
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

        return random.randint(max(age,table[period-1]*12),table[period]*12)

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
        self.mourning=roud_well(math.log(t,math.e))/-l
        
    def one_more_month(self):
        self.age+=1
        if self.age==12*12 or self.age==15*12 or self.age==21*12 or self.age==35*12 or self.age==45*12 or self.age==60*12:
            self.wtbiac=self.c_wtbiac(self.age)
        self.mourning= max(0 ,self.mourning-1)
class Population:
    def __init__(self,m,f,years=100):
        # 0 is male, 1 es female
        self.men=[Person(0) for _ in range(m)]
        self.women=[Person(1) for _ in range(f)]
        self.time=years*12
        #couples to break
        self.couples=[]
        #number of couples
        self.noc=0


    def remove_dead_people(self):
        i=0
        while(i<len(self.men)):
            if self.men[i].is_dead():
                self.men.remove(self.men[i])
            else:
                i+=1   
        i=0
        while(i<len(self.women)):
            if self.women[i].is_dead():
                self.women.remove(self.women[i])
            else:
                i+=1 

    def run(self):
        self.remove_dead_people()
        count=0
        while self.time!=0:
            for i in self.men:
                i.one_more_month()
            for i in self.women:
                i.one_more_month()
            self.remove_dead_people()
            for i in self.couples:
                i[2]-=1
            self.remove_couples()
            self.make_couples()
            if count%12==0:
                print(len(self.men),len(self.women),len(self.couples),self.noc)
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
                self.couples.append([am,aw,t3])
            else:
                self.couples.append([am,aw,min(t1,t2)])
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
               
                       
a=Population(1000,1000,126)
a.run()
















