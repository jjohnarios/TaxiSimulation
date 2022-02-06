from time_point import TimePoint
import numpy as np
import queue
import logging


logging.basicConfig(filename="a.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

def taxi_id_number(num_taxis):
    '''
    Yields a generator as an id for each taxi.
    This will iterate until it has emitted num_taxis numbers (next()).
    '''
    arr=np.arange(num_taxis)
    np.random.shuffle(arr) #shuffle
    for i in range(num_taxis):
        yield arr[i]

def shift_info():
    '''
    Info about shifts.
    Yields a generator as (starting time, ending time, mean shift trips).
    We make the assumption that there are more taxis/shifts in the middle of the day.
    '''
    start_times_and_freqs=[(0,8),(8,30),(16,15)] # 00:00 - 08:00 x8 mean shift trips, 08:00-16:00 x30 mean shift trips, 16:00 - 00:00 x15 mean shift trips 
    indices=np.arange(len(start_times_and_freqs))
    while True:
        idx=np.random.choice(indices,p=[0.25,0.5,0.25]) #Bigger probability in the middle of the day
        start=start_times_and_freqs[idx]
        yield(start[0],start[0]+8,start[1])

def process_taxi(taxi_id_generator,shift_info_generator):
    '''
    Yields generators to indicate the shifts of a taxi cab.
    delta time could be simplified even more.
    '''
    taxi_id=next(taxi_id_generator)
    shift_start,shift_end,shift_mean_trips=next(shift_info_generator)
    
    actual_trips=round(np.random.normal(loc=shift_mean_trips))
    average_trip_time= (7.0 / shift_mean_trips) * 60 # Mean trip time in minutes,7=8hours -1hour "lost time"
    between_events_time=1.0/(shift_mean_trips-1) * 60  #this is an efficient city where cabs are seldom unused

    #Shift starts
    time=shift_start
    yield TimePoint(taxi_id, 'start shift', time)
    deltaT=np.random.poisson(between_events_time) / 60
    time+=deltaT

    # For every trip pick a customer then drop them off then pick another one etc.
    for i in range(actual_trips):
        yield TimePoint(taxi_id,'pick up',time)
        deltaT=np.random.poisson(average_trip_time)/60
        time+=deltaT
        yield TimePoint(taxi_id,'drop off',time)
        deltaT=np.random.poisson(between_events_time) / 60
        time+=deltaT
    
    deltaT=np.random.poisson(between_events_time) / 60
    time+=deltaT
    yield TimePoint(taxi_id,'end shift',time)

class Simulator:

    def __init__(self,num_taxis):
        self._time_points=queue.PriorityQueue() # Time Points are pushed into a priority queue
        taxi_id_generator=taxi_id_number(num_taxis)
        shift_info_generator=shift_info()
        self._taxis=[]
        for i in range(num_taxis):
            self._taxis.append(process_taxi(taxi_id_generator,shift_info_generator))

        self._prepare_run()

        
    
    def _prepare_run(self):
        for t in self._taxis:
            while True:
                try:
                    e=next(t)
                    self._time_points.put(e)
                except:
                    break
    
    def run(self):
        simulation_time=0
        while simulation_time <24:
            if self._time_points.empty():
                break
            p= self._time_points.get()
            simulation_time=p.time
            logging.info(p)
        

if __name__=="__main__":

    sim=Simulator(1000)
    sim.run()