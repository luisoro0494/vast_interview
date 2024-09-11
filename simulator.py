from lunar_mining_truck import mining_truck as n_truck
from stations import unload_stations as m_unload_station
from station_manager import station_manager

import random
import logging

logger = logging.getLogger(__name__)
class lunar_Helium_3_sim:
    '''

    '''

    def __init__(self,
                num_mining_trucks : int,
                num_unload_stations : int,
                sim_duration_hrs : int,
                truck_unload_duration : int,
                mining_duration_min_hrs : int,
                mining_duration_max_hrs : int):

        self.num_mining_trucks = num_mining_trucks
        self.num_unload_stations = num_unload_stations
        self.mining_duration_min = mining_duration_min_hrs*60
        self.mining_duration_max = mining_duration_max_hrs*60
        # convert time to minutes
        self.sim_duration = sim_duration_hrs * 60
        
        # completed loads
        self.total_loads = 0

        self.truck_unload_duration = 5
        self.mining_trucks = []
        self.unloading_stations = []
    
        self.station_manager = None


    def create_stations(self):
        return [m_unload_station(station_ID=m) for m in range(self.num_unload_stations)]

    def create_trucks(self):

        for n in range(self.num_mining_trucks):
            truck_mining_duration = random.randint(self.mining_duration_min,
                                                    self.mining_duration_max)

            self.mining_trucks.append(n_truck(truck_ID = n, 
                                        stations = self.unloading_stations,
                                        mining_duration = truck_mining_duration, 
                                        unload_duration = self.truck_unload_duration,
                                        station_manager = self.station_manager))

        return self.mining_trucks

    def run(self):
        # initialize trucks
        self.unloading_stations = self.create_stations()
        self.station_manager = station_manager(self.unloading_stations)
        self.mining_trucks = self.create_trucks()

        current_time = 0
        # Start state machine
        while current_time < self.sim_duration:

            logger.info(f"current time is: {current_time}")
            if current_time == 0:
                # set all initial states to start_mining
                for truck in self.mining_trucks:
                    truck.update_current_time(current_time)
                    truck.start_mining()
            else:
                # update the current time and run the current state
                for truck in self.mining_trucks:
                    truck.update_current_time(current_time)
                    truck.state()
                # if there is a truck in a queue, serve it next
                truck_in_queue, station = self.station_manager.manage_queue()
                if truck_in_queue is not None:
                    self.mining_trucks[truck_in_queue].unloading()

            # update time (every minute)
            current_time += 1

        # Print out total loads
        for truck in self.mining_trucks:
            logger.info(f"Truck ({truck.ID}) unloaded: {truck.get_completed_load_count()} loads")
            self.total_loads += truck.get_completed_load_count()
        
        logger.info(f"Total loads completed with {self.num_mining_trucks} trucks and {self.num_unload_stations} unload stations: {self.total_loads}")
        
        return self.total_loads

    