
import logging
logger = logging.getLogger(__name__)

class mining_truck:
    """
    Represents a lunar mining truck.

    This mining truck class has 6 different states defined. Each state represents
    a step in the mining process. Each state has conditions defined on when to go
    to the next state.

    Attributes:
        truck_ID (int): Current Truck ID.
        stations (list): List of unloading_stations objects.
        unload_duration (int): Unloading duration at station.
        travel_to_unload (int): Travel to unload station duration.
        mining_duration (int): Mining duration.
        station_manager (object): station_manager object.

    Methods:
        update_current_time(): Updates the current time on the truck state machine.
        get_completed_load_count(): Returns a sum of all loads completed by truck instance.

        start_mining(): First state on the mining process. 
        mining_in_progress(): Second state in mining process.
        travel_to_unload(): Third state in mining process.
        wait_to_unload(): Fourth state in mining process.
        unloading(): Fifth state in mining process.
        load_complete(): Final state in mining process.

        check_for_station_availability(): Returns ture if station is available, else returns False
    """

    def __init__(self,
                truck_ID : int,
                stations : list,
                unload_duration : int,
                travel_to_unload: int,
                mining_duration : int,
                station_manager : object):
        """
        Initializes the mining_truck class with simulator parameters.

        Args:
            truck_ID (int): Current Truck ID.
            stations (list): List of unloading_stations objects.
            unload_duration (int): Unloading duration at station.
            travel_to_unload (int): Travel to unload station duration.
            mining_duration (int): Mining duration.
            station_manager (object): station_manager object.
        """
        # Initialize all variables
        self.ID = truck_ID
        self.stations_list = stations
        self.unload_duration = unload_duration
        self.mining_duration = mining_duration
        self.travel_to_unload_duration = travel_to_unload
        self.station_manager = station_manager

        self.current_time = None
        self.operation_start_time = None
        self.unload_start_time = None
        self.time_elapsed_unloading = 0
        self.time_elapsed_mining = 0
        self.time_elapsed_traveling = 0
        self.completed_load_count = 0
        self.assigned_station = None

        # Set initial state to start_mining
        self.state = self.start_mining

    def update_current_time(self, current_time : int) -> None:
        """
        Updates the current time on the truck state machine.

        Args:
            current_time (int): current time from simulator
        Returns:
            None
        """ 
        self.current_time = current_time

    def get_completed_load_count(self) -> int:
        """
        Returns a sum of all loads completed by truck instance.

        Returns:
            int: Returns completed load count.
        """ 
        return self.completed_load_count

    def start_mining(self) -> None:
        """
        First state in the mining process. Always goes to next state (mining_in_progress)

        Returns:
            None
        """ 
        # set operation_start_time to current time
        self.operation_start_time = self.current_time
        logger.info(f"Truck ({self.ID}) is going to start mining with a duration time of {self.mining_duration}")
        # next state
        self.state = self.mining_in_progress
        
    def mining_in_progress(self) -> None:
        """
        Second state in the mining process. Goes to next state (travel_to_unload) when it completes
        a mining operation. It will remain in this state until the time elapsed has reached the
        mining duration.

        Returns:
            None
        """ 
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

    def travel_to_unload(self) -> None:
        """
        Third state in the mining process. Goes to next state (wait_to_unload) when it reaches
        the mining travel duration. It will remain in this state until the time elapsed has reached the
        travel duration.

        Returns:
            None
        """ 
        self.time_elapsed_traveling = self.current_time - self.operation_start_time
        logger.info(f"Truck ({self.ID}) is traveling to unload site with elapsed time of: {self.time_elapsed_traveling}")
        
        if self.time_elapsed_traveling < self.travel_to_unload_duration:
            self.state = self.travel_to_unload
        else:
            self.time_elapsed_traveling = 0
            # next state
            self.state = self.wait_to_unload

    def wait_to_unload(self) -> None:
        """
        Fourth state in the mining process. Goes to next state (unloading) when a station
        becomes available. It will remain in this state until a station with the least amount of
        trucks in queue becomes available.

        Returns:
            None
        """ 
        logger.info(f"Truck ({self.ID}) is in waiting to unload")
        if self.check_for_station_availability():
            # go to next state
            logger.info(f"Truck ({self.ID}) is unloading now.")

            self.operation_start_time = self.current_time
            self.state = self.unloading
        else:
            self.state = self.wait_to_unload
    
    def unloading(self) -> None:
        """
        Fifth state in the mining process. Goes to next state (load_complete) when time elapsed
        has reached unloading duration. It will remain in this state until unloading duration has
        been reached.

        Returns:
            None
        """ 
        if self.time_elapsed_unloading < self.unload_duration:
            logger.info(f"Truck ({self.ID}) is unloading with elapsed time of {self.time_elapsed_unloading} at station ({self.assigned_station})")
            self.time_elapsed_unloading += 1
            self.state = self.unloading
        else:
            # next state
            logger.info(f"Truck ({self.ID}) is done unloading.")
            self.state = self.load_complete

    def load_complete(self) -> None:
        """
        Sixth state in the mining process. Always goes to next state (load_complete).
        It releases the current unloading station and keeps count of loads completed
        by truck instance.

        Returns:
            None
        """ 
        # restart elapsed unloading time 
        self.time_elapsed_unloading = 0

        logger.debug(f"releasing station ({self.assigned_station})")
        self.station_manager.release_station(self.assigned_station)   

        self.completed_load_count += 1
        logger.info(f"Truck ({self.ID}) has completed {self.completed_load_count} loads.")

        # next state
        self.state = self.start_mining

    def check_for_station_availability(self) -> bool:
        """
        Checks if there is any available stations and returns station with the least
        amount of trucks in queue.

        Returns:
            bool: True if there is a station available, False if none available.
        """ 
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
