import logging
logger = logging.getLogger(__name__)

class station_manager:
    """
    Represents a station manager.

    While running a simulation, this class manages each station in the simulation.
    This class manages availability of each station and queues statios
    when not available.

    Attributes:
        stations (list): A list of station objects.

    Methods:
        get_available_station(): returns first available station.
        queue_truck(): queues truck inot station's queue list parameter.
        release_station(): releases station by setting available flag to True.
        block_station(): blocks station from being used.
        manage_queue(): checks if any station has a queue and is available to
                        serve the next truck in queue.
    """
    def __init__(self, stations):
        self.stations = stations
        """
        Initializes the station_manager class with a list of station objects.

        Args:
            stations (list): A list of station objects.
        """
    def get_available_station(self) -> object:
         """
        Find and return an available station with no queue
        
        Returns:
            unload_stations: Returns an unload_stations object.
        """
        for station in self.stations:
            if station.is_available and not station.truck_queue:
                # station.is_available = False
                return station
        return None

    def queue_truck(self, truck_id : int) -> object:
        """
        Queue truck at the station with the smallest queue

        Args:
            truck_id (int): Truck ID to queue.
        Returns:
            unload_stations: Returns an unload_stations object with the smallest queue.
        """

        # check if truck_id is already in any of the station queues. Avoids duplicates.
        id_already_in_queue = any(truck_id in station.truck_queue for station in self.stations)
        if truck_id and not id_already_in_queue:
            station_with_least_queue = min(self.stations, key=lambda station: len(station.truck_queue))
            station_with_least_queue.queue_truck(truck_id)
        else:
            logger.info(f"Truck ({truck_id}) is already in the queue.")
            return None
        return station_with_least_queue

    def release_station(self, station_id : int) -> None:
        """
        Makes the input station available to use.

        Args:
            station_id (int): Station ID to queue.
        Returns:
            None
        """
        self.stations[station_id].is_available = True

    def block_station(self, station_id : int) -> None:
        """
        Blocks the input station from being available to use.

        Args:
            station_id (int): Station ID to queue.
        Returns:
            None
        """ 
        self.stations[station_id].is_available = False

    def manage_queue(self) -> tuple:
        """
        Blocks the input station from being available to use.

        Returns:
            tuple: Tuple containing
                - object: truck_in_queue
                - object: unload_stations instance
        """ 

        for station in self.stations:
            if station.truck_queue:
                logger.debug(f"Truck queue at station ({station.ID} is: {station.truck_queue})")

            if station.truck_queue and station.is_available:
                truck_in_queue = station.dequeue_truck()
                station.is_available = False
                return truck_in_queue, station

        return None, None
