class unload_stations:

    def __init__(self,
                station_ID : int,
                truck_ID : int = None):

        self.ID = station_ID
        self.truck_ID = truck_ID

        self.is_available = True
        self.truck_queue = []
    
    def assign_truck(self, truck_ID : int):

        self.truck_ID = truck_ID
        self.is_available = False

    def remove_truck(self, truck_ID : int):

        self.truck_ID = None
        self.is_available = True

    def queue_truck(self, truck_ID : int):

        self.truck_queue.append(truck_ID)
        # self.is_available = False

    def dequeue_truck(self):
        '''
        
        '''
        if self.truck_queue:
            return self.truck_queue.pop(0)
        return None  # Return None if no trucks are in queue