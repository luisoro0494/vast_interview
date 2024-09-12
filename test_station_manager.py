import pytest
from station_manager import station_manager
from lunar_mining_truck import mining_truck
from stations import unload_stations as m_unload_station

def create_stations(num_stations) -> list:
    """
    Generates a list of unloading_stations objects.

    Returns:
        list: list of unloading_stations objects
    """
    return [m_unload_station(station_ID=i) for i in range(num_stations)]

def test_assign_truck_to_station() -> None:
    """
    Test to ensure station assignment works and trucks are assigned correctly

    Returns:
        None
    """
    # Create 2 stations
    stations = create_stations(2)
    s_m = station_manager(stations)
    
    # Create two trucks
    truck_1 = mining_truck(truck_ID=1, stations=stations, unload_duration=5, travel_to_unload = 30, mining_duration=10, station_manager=s_m)
    truck_2 = mining_truck(truck_ID=2, stations=stations, unload_duration=5, travel_to_unload = 30, mining_duration=10, station_manager=s_m)

    # Assign truck 1 to a station
    assigned_station = s_m.get_available_station()
    assert assigned_station is not None, "Truck 1 should be assigned to a station."
    truck_1.assigned_station = assigned_station.ID
    assigned_station.assign_truck(truck_1.ID)

    # Ensure the station is now unavailable
    assert not assigned_station.is_available, f"Station {assigned_station.ID} should now be unavailable."

    # Try assigning truck 2 to a station
    next_station = s_m.get_available_station()
    assert next_station is not assigned_station, "Truck 2 should be assigned to a different station."

def test_no_duplicate_queue() -> None:
    """
    Test to ensure a truck is not added to the same queue twice

    Returns:
        None
    """

    # Create 1 station
    stations = create_stations(1)
    s_m = station_manager(stations)

    # Create a truck
    truck_1 = mining_truck(truck_ID=1, stations=stations, unload_duration=5, travel_to_unload = 30, mining_duration=10, station_manager=s_m)

    # Queue truck 1
    s_m.queue_truck(truck_1.ID)

    # Queue truck 1 again (should not be added again)
    s_m.queue_truck(truck_1.ID)

    # Check that truck_1 only appears once in the queue
    assert len(stations[0].truck_queue) == 1, "Truck 1 should only be in the queue once."

def test_manage_queue() -> None:
    """
    Test queue management to ensure trucks are dequeued properly

    Returns:
        None
    """
    # Create 1 station
    stations = create_stations(1)
    s_m = station_manager(stations)

    # Create two trucks
    truck_1 = mining_truck(truck_ID=1, stations=stations, unload_duration=5, travel_to_unload = 30, mining_duration=10, station_manager=s_m)
    truck_2 = mining_truck(truck_ID=2, stations=stations, unload_duration=5, travel_to_unload = 30, mining_duration=10, station_manager=s_m)

    # Queue both trucks
    s_m.queue_truck(truck_1.ID)
    s_m.queue_truck(truck_2.ID)

    # Dequeue the first truck
    truck_in_queue, station = s_m.manage_queue()
    assert truck_in_queue == truck_1.ID, "Truck 1 should be dequeued first."
    assert not station.is_available, "Station should be unavailable after truck is dequeued."

    # Complete unloading for truck 1 and release the station
    s_m.release_station(station.ID)
    
    # Dequeue the second truck
    truck_in_queue, station = s_m.manage_queue()
    assert truck_in_queue == truck_2.ID, "Truck 2 should be dequeued second."
    assert not station.is_available, "Station should remain unavailable after dequeuing the second truck."

def test_release_station() -> None:
    """
    Test station release after truck unload

    Returns:
        None
    """
    # Create 1 station
    stations = create_stations(1)
    s_m = station_manager(stations)

    # Create a truck
    truck_1 = mining_truck(truck_ID=1, stations=stations, unload_duration=5, travel_to_unload = 30, mining_duration=10, station_manager=s_m)

    # Assign truck to a station
    station = s_m.get_available_station()
    assert station is not None, "Station should be available."
    truck_1.assigned_station = station.ID
    station.assign_truck(truck_1.ID)

    # Truck completes unloading and releases the station
    s_m.release_station(truck_1.assigned_station)

    # Ensure the station is available again
    assert station.is_available, "Station should be available after release."

    # Ensure station's trucks served counter works
    assert station.get_total_trucks_served() == 1, "Station should only have 1 served truck in counter."
