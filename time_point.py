from dataclasses import dataclass
import datetime

'''
@dataclass is a decorator which adds various "dunder"(double under __func__)
methods to the class.

The corresponding __init__ method of that class would be:

def __init__(self,taxi_id:int,name:str,time:float):
    
    self.taxi_id= taxi_id
    self.name=name
    self.time=time

'''


@dataclass
class TimePoint:
    taxi_id: int
    name:  str
    time: float


    def __lt__(self,other):
        #overwriting Lower Than method
        return self.time < other.time
    
    def __str__(self):
        #overwriting str method
        return "Taxi id: "+ str(self.taxi_id) + " Name: " + self.name + " Time: " + str(datetime.timedelta(hours=self.time))[:-3]