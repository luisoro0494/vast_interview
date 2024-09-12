class unload_stations:
    """
    Represents an unloading station.

    Unloading station class with for managing state of each station.

    Attributes:
        station_ID (int): Station ID.
        truck_ID (int): Truck ID for truck assignment to station (Optional).

    Methods:
        assign_truck(): Assignes input truck ID to station.
        remove_truck(): Removes assigned truck from station.
        queue_truck(): Appends input truck to the truck_queue.
        dequeue_truck(): Dequeues truck from station's truck_queue.
        add_to_served_counter():  Adds to total trucks served counter.
        get_total_trucks_served(): Returns total trucks served in station instance.
    """
    def __init__(self,
                station_ID : int,
                truck_ID : int = None):
        """
        Initializes the unload_stations class with a input station ID.

        Args:
            station_ID (int): Current station ID.
        """
        self.ID = station_ID
        self.truck_ID = truck_ID

        self.is_available = True
        self.truck_queue = []
        self.truck_count = 0

    def assign_truck(self, truck_ID : int) -> None:
        """
        Assignes input truck ID to station.

        Args:
            truck_ID (int): Current truck ID.
        """

        self.truck_ID = truck_ID
        self.is_available = False

    def remove_truck(self, truck_ID : int) -> None:
        """
        Removes input truck ID from station and sets availability to False.

        Args:
            truck_ID (int): Current truck ID.
        """

        self.truck_ID = None
        self.is_available = True

    def queue_truck(self, truck_ID : int) -> None:
        """
        Appends input truck to the truck_queue..

        Args:
            truck_ID (int): Current truck ID.
        """
        self.truck_queue.append(truck_ID)

    def dequeue_truck(self) -> object:
        """
        Dequeues input truck from the truck_queue.

        Return:
            mining_truck: mining truck that was first in queue.
        """
        if self.truck_queue:
            return self.truck_queue.pop(0)
        return None  # Return None if no trucks are in queue

    def add_to_served_counter(self) -> None:
        """
        Adds to total trucks served counter.

        Return:
            None
        """
        self.truck_count += 1

    def get_total_trucks_served(self) -> int:
        """
        Returns total trucks served in station instance.

        Return:
            int: total count of trucks served
        """
        return self.truck_count