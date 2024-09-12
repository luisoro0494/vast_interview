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
