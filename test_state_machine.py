from stations import unload_stations as m_unload_station
from lunar_mining_truck import mining_truck as n_truck
from station_manager import station_manager

import random
import pytest

mining_duration_min_hrs = 1
mining_duration_max_hrs = 5
num_mining_trucks = 20
mining_trucks = []
unloading_stations = []
num_unload_stations = 2
truck_unload_duration = 5
sim_duration_hrs = 72

def create_stations(num_unload_stations : int) -> list:
    """
    Generates a list of unloading_stations objects.

    Returns:
        None
    """
    return [m_unload_station(station_ID=m) for m in range(num_unload_stations)]

def test_state_transition() -> None:
    """
    Runs each test case for each state in the mining process. 

    Returns:
        None
    """
    stations = create_stations(2)
    s_m = station_manager(stations)
    
    # Create two trucks
    truck_1 = n_truck(truck_ID=1, stations=stations, unload_duration=5, travel_to_unload = 30, mining_duration=10, station_manager=s_m)
    truck_2 = n_truck(truck_ID=2, stations=stations, unload_duration=5, travel_to_unload = 30, mining_duration=10, station_manager=s_m)

    # initialize current time on truck 1
    truck_1.update_current_time(0)

    # set state to initial state
    truck_1.start_mining()

    assert truck_1.state == truck_1.mining_in_progress, "Truck 1 next state should be mining_in_progress"

    # check that the state doesn't change if truck is not done mining
    truck_1.update_current_time(9)
    truck_1.mining_in_progress()
    assert truck_1.state == truck_1.mining_in_progress, "Truck 1 next state should be mining_in_progress"

    # trigger next state conditions
    truck_1.update_current_time(11)
    truck_1.mining_in_progress()
    assert truck_1.state == truck_1.travel_to_unload, "Truck 1 next state should be travel_to_unload"


    # check that the state doesn't change if truck is not done traveling
    truck_1.update_current_time(29) 
    truck_1.travel_to_unload()
    assert truck_1.state == truck_1.travel_to_unload, "Truck 1 next state should be travel_to_unload"

    # trigger next state conditions
    truck_1.update_current_time(30) # takes 30 minutes to travel
    truck_1.operation_start_time = 0 # forcing start time back to 0
    truck_1.travel_to_unload()
    assert truck_1.state == truck_1.wait_to_unload, "Truck 1 next state should be wait_to_unload"

    # check that the state doesn't change if truck is there is no available station
    for station in stations:
        station.is_available = False
    truck_1.wait_to_unload()
    assert truck_1.state == truck_1.wait_to_unload, "Truck 1 next state should be wait_to_unload"
    assert truck_1.ID in stations[0].truck_queue, "Station 0 should have Truck_1 ID in queue"

    # trigger next state conditions
    stations[1].is_available = True
    truck_1.wait_to_unload()
    assert truck_1.state == truck_1.unloading, "Truck 1 next state should be unloading"

    # check that the state doesn't change if time unloading is under set unload time
    truck_1.time_elapsed_unloading = 3
    truck_1.unloading()
    assert truck_1.state == truck_1.unloading, "Truck 1 next state should be unloading"
    
    # trigger next state conditions
    truck_1.time_elapsed_unloading = 5
    truck_1.unloading()
    assert truck_1.state == truck_1.load_complete, "Truck 1 next state should be load_complete"
    
    # trigger final state
    truck_1.load_complete()
    assert truck_1.state == truck_1.start_mining, "Truck 1 next state should be start mining"

