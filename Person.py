import random
import math
import collections
import matplotlib.pyplot as plt
from utils import round_well

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
        self.mourning=round_well(math.log(t,math.e)/-l)
        
    def one_more_month(self):
        self.age+=1
        if self.age==12*12 or self.age==15*12 or self.age==21*12 or self.age==35*12 or self.age==45*12 or self.age==60*12:
            self.wtbiac=self.c_wtbiac(self.age)
        self.mourning= max(0 ,self.mourning-1)
        self.birth_time= max(0 ,self.birth_time-1)
