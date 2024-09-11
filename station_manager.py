import logging
logger = logging.getLogger(__name__)
class station_manager:
    def __init__(self, stations):
        self.stations = stations

    def get_available_station(self):
        # Find and return an available station with no queue
        for station in self.stations:
            if station.is_available and not station.truck_queue:
                # station.is_available = False
                return station
        return None

    def queue_truck(self, truck_id):
        # Queue truck at the station with the smallest queue
        
        # station_with_least_queue.queue_truck(truck_id)
                # Check if the truck is already in the queue for the station
        id_already_in_queue = any(truck_id in station.truck_queue for station in self.stations)
        if truck_id and not id_already_in_queue:
            station_with_least_queue = min(self.stations, key=lambda station: len(station.truck_queue))
            station_with_least_queue.queue_truck(truck_id)
        else:
            logger.info(f"Truck ({truck_id}) is already in the queue.")
            return None
        return station_with_least_queue

    def release_station(self, station_id):
        # Make the station available
        self.stations[station_id].is_available = True

    def block_station(self, station_id):
        # Make the station available
        self.stations[station_id].is_available = False

    def manage_queue(self):
        for station in self.stations:
            if station.truck_queue:
                logger.debug(f"Truck queue at station ({station.ID} is: {station.truck_queue})")
            if station.truck_queue and station.is_available:
                truck_in_queue = station.dequeue_truck()
                station.is_available = False
                return truck_in_queue, station
        return None, None
