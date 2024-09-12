# Lunar Helium-3 Mining Simulation

This repository contains a Python simulation for a lunar Helium-3 space mining operation. The simulation manages mining trucks and unload stations to track performance metrics over a 72-hour simulation.

## Project Structure

- **`lunar_mining_truck.py`**: Contains the logic for mining trucks.
- **`stations.py`**: Defines the unload stations and their behaviors.
- **`station_manager.py`**: Manages the stations and handles truck queues.
- **`simulator.py`**: The main simulation logic.
- **`run_sim.py`**: Script to run the simulation and collect results.
- **`log_setup.py`**: Configures logging for the simulation.

## How to Run the Project

1. **Install dependencies**:
   Ensure you have Python installed and run the following to install the required packages:
   ```bash
   pip install -r requirements.txt

2. **Configuration**:
    You can configure the number of trucks, stations, and other parameters in the run_sim.py file:
    ```bash
    sim_1 = lunar_Helium_3_sim(
    num_mining_trucks=10,
    num_unload_stations=2,
    sim_duration_hrs=72,
    truck_unload_duration=5,
    travel_to_unload=30,
    mining_duration_min_hrs=1,
    mining_duration_max_hrs=5
    )

3. **Run the simulations**:
    To run a simulation with the default configuration, use the following command:
    ```bash
    python run_sim.py

## Example Output

You can view an example of the simulation's log output by following [this link](https://raw.githubusercontent.com/luisoro0494/vast_interview/main/2024-09-12-01-01_lunar_helium_3_sim.log).


## Unit Testing

To run unit tests, run the following commands:
```bash
    pytest test_state_machine.py
    pytest test_station_manager.py
```

## Design Approach

I used a state machine to simulate the mining operation, with trucks cycling through states like mining, traveling, and unloading. This approach simplifies future modifications by isolating the logic for each state.

Each truck mines for a random duration (1-5 hours), then travels to an unload station (30 minutes) to unload (5 minutes). If stations are occupied, trucks are added to a queue.

A Station Manager handles the queuing, tracking the status of each station and assigning trucks to the station with the shortest queue. Once a station becomes available, it serves the first truck in line.

At the end of the simulation, a report logs key statistics:

 - Truck performance: Number of completed loads and time spent in each state.
 - Station performance: Utilization and queue lengths.

This design is flexible and can easily accommodate future changes, such as modifying queuing logic or adding prioritization.

Future Design Improvements:
 - Adjust the user interface based on the target audience:
    - For example, if the end user isn’t familiar with code, the configuration could be managed through a .yml file to avoid direct interaction with the source code.
 - Enhance the statistics report to include more detailed output, with the option to export the data to a CSV file, controlled via the configuration file.