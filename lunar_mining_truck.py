
import logging
logger = logging.getLogger(__name__)
class mining_truck:

    TRAVEL_TO_UNLOAD_TIME = 30 # minutes

    def __init__(self,
                truck_ID : int,
                stations : list,
                unload_duration : int,
                mining_duration : int,
                station_manager : object):

        self.ID = truck_ID
        self.stations_list = stations

        self.state = self.start_mining
        self.current_time = None
        self.operation_start_time = None

        self.unload_start_time = None

        self.unload_duration = unload_duration
        self.mining_duration = mining_duration
        self.time_elapsed_unloading = 0
        self.time_elapsed_mining = 0
        self.time_elapsed_traveling = 0
        self.completed_load_count = 0
        self.assigned_station = None

        self.station_manager = station_manager

    def update_current_time(self, current_time):
        self.current_time = current_time

    def get_completed_load_count(self) -> int:
        return self.completed_load_count

    def start_mining(self):

        self.operation_start_time = self.current_time
        logger.info(f"Truck ({self.ID}) is going to start mining with a duration time of {self.mining_duration}")
        # next state
        self.state = self.mining_in_progress
        
    
    def mining_in_progress(self):

        self.time_elapsed_mining = self.current_time - self.operation_start_time

        if self.time_elapsed_mining < self.mining_duration:
            logger.info(f"Truck ({self.ID}) is mining with elapsed time of: {self.time_elapsed_mining}")
            self.state = self.mining_in_progress
        else:
            logger.info(f"Truck ({self.ID}) is done mining.")
            # restart elapsed mining time and set next state
            self.time_elapsed_mining = 0
            # reset start time
            self.operation_start_time = self.current_time
            # next state
            self.state = self.travel_to_unload

    def travel_to_unload(self):
        
        self.time_elapsed_traveling = self.current_time - self.operation_start_time
        logger.info(f"Truck ({self.ID}) is traveling to unload site with elapsed time of: {self.time_elapsed_traveling}")
        if self.time_elapsed_traveling < self.TRAVEL_TO_UNLOAD_TIME:
            # self.time_elapsed_traveling += 1
            self.state = self.travel_to_unload
        else:
            self.time_elapsed_traveling = 0
            # next state
            self.state = self.wait_to_unload

    def wait_to_unload(self):
        
        logger.info(f"Truck ({self.ID}) is in waiting to unload")
        if self.check_for_station_availability():
            # go to next state
            logger.info(f"Truck ({self.ID}) is unloading now.")

            self.operation_start_time = self.current_time
            self.state = self.unloading
        else:
            self.state = self.wait_to_unload
    
    def unloading(self):

        if self.time_elapsed_unloading < self.unload_duration:
            logger.info(f"Truck ({self.ID}) is unloading with elapsed time of {self.time_elapsed_unloading} at station ({self.assigned_station})")
            # self.station_manager.block_station(self.assigned_station)
            self.time_elapsed_unloading += 1
            self.state = self.unloading
        else:
            # restart elapsed unloading time and set next state
            logger.info(f"Truck ({self.ID}) is done unloading.")
            self.state = self.load_complete

    def load_complete(self):
        
        self.time_elapsed_unloading = 0
        self.state = self.start_mining
        logger.debug(f"releasing station ({self.assigned_station})")
        self.station_manager.release_station(self.assigned_station)          
        self.completed_load_count += 1
        logger.info(f"Truck ({self.ID}) has completed {self.completed_load_count} loads.")

    def check_for_station_availability(self) -> bool:
        # Ask StationManager for an available station
        available_station = self.station_manager.get_available_station()
        
        if available_station:
            if self.ID in available_station.truck_queue:
                return False
            
            # Assign the truck to the available station
            available_station.assign_truck(self.ID)
            self.assigned_station = available_station.ID
            logger.info(f"Truck ({self.ID}) is going to start unloading at station ({available_station.ID})")
            return True
        
        # If no available station, queue the truck at the station with the least queue
        station_with_least_queue = self.station_manager.queue_truck(self.ID)
        if not station_with_least_queue:
            pass
        else:
            self.assigned_station = station_with_least_queue.ID
        logger.info(f"Truck ({self.ID}) is currently in the queue for station ({self.assigned_station}).")
        
        return False
