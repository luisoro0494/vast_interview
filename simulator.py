from lunar_mining_truck import mining_truck as n_truck
from stations import unload_stations as m_unload_station
from station_manager import station_manager

import random
import logging

logger = logging.getLogger(__name__)
class lunar_Helium_3_sim:
    """
    Represents a Lunar Helium-3 Simulator.

    This class creates the simulation environment of a lunar Helium-3 mining
    operation. This simulation will manage and track the efficiency of mining 
    trucks and unload stations over a continuous operation.

    Attributes:
        num_mining_trucks (int): Number of mining trucks in operation.
        num_unload_stations (int): Number of unloading stations in operation.
        sim_duration_hrs (int): Simulator duration in hours.
        truck_unload_duration (int): Truck unloading duration in minutes.
        travel_to_unload (int): Travel to unload duration in minutes.
        mining_duration_min_hrs (int): Mining duration minimum amount of hours.
        mining_duration_max_hrs (int): Mining duration max amount of hours.
    Methods:
        create_stations(): Generates a list of unloading_stations objects.
        create_trucks(): Generates a list of mining_truck objects.
        run(): Runs simulaiton.
    """

    def __init__(self,
                num_mining_trucks : int,
                num_unload_stations : int,
                sim_duration_hrs : int,
                truck_unload_duration : int,
                travel_to_unload : int,
                mining_duration_min_hrs : int,
                mining_duration_max_hrs : int):
        """
        Initializes the lunar_Helium_3_sim class with all simulator attributes.

        Args:
            num_mining_trucks (int): Number of mining trucks in operation.
            num_unload_stations (int): Number of unloading stations in operation.
            sim_duration_hrs (int): Simulator duration in hours.
            truck_unload_duration (int): Truck unloading duration in minutes.
            travel_to_unload (int): Travel to unload duration in minutes.
            mining_duration_min_hrs (int): Mining duration minimum amount of hours.
            mining_duration_max_hrs (int): Mining duration max amount of hours.
        """
        
        self.num_mining_trucks = num_mining_trucks
        self.num_unload_stations = num_unload_stations
        self.truck_unload_duration = truck_unload_duration
        self.travel_to_unload = travel_to_unload

       # convert time to minutes
        self.mining_duration_min = mining_duration_min_hrs * 60
        self.mining_duration_max = mining_duration_max_hrs * 60
        self.sim_duration = sim_duration_hrs * 60
        
        # initialize variables
        self.total_loads = 0
        self.mining_trucks = []
        self.unloading_stations = []
        self.station_manager = None


    def create_stations(self) -> None:
        """
        Generates a list of unloading_stations objects.

        Returns:
            None
        """
        return [m_unload_station(station_ID=m) for m in range(self.num_unload_stations)]

    def create_trucks(self) -> None:
        """
        Generates a list of mining_truck objects.

        Returns:
            None
        """
        for n in range(self.num_mining_trucks):
            truck_mining_duration = random.randint(self.mining_duration_min,
                                                    self.mining_duration_max)

            self.mining_trucks.append(n_truck(truck_ID = n, 
                                        stations = self.unloading_stations,
                                        mining_duration = truck_mining_duration, 
                                        travel_to_unload = self.travel_to_unload,
                                        unload_duration = self.truck_unload_duration,
                                        station_manager = self.station_manager))

        return self.mining_trucks

    def run(self):
        """
        Runs Simulation.

        Returns:
            None
        """
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

        for station in self.unloading_stations:
            logger.info(f"Station ({station.ID}) served: {station.get_total_trucks_served()} trucks")

        logger.info(f"Total loads completed with {self.num_mining_trucks} trucks and {self.num_unload_stations} unload stations: {self.total_loads}")
        
        return self.total_loads

    