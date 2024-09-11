# import yaml
import logging
from datetime import datetime

from simulator import lunar_Helium_3_sim

# Configure the logger
log_name = datetime.now().strftime("%Y-%m-%d-%H-%M_lunar_helium_3_sim.log")
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler(log_name),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)
# with open("./configs/config_1.yml", "r") as file:
#     # Load the YAML content into a Python dictionary
#     config = yaml.safe_load(file)

sim_1 = lunar_Helium_3_sim(
                num_mining_trucks = 10,
                num_unload_stations = 2,
                sim_duration_hrs = 72,
                truck_unload_duration = 5,
                mining_duration_min_hrs = 1,
                mining_duration_max_hrs = 5)

results = []
for i in range(1):
    sim_1 = lunar_Helium_3_sim(
                    num_mining_trucks = 10,
                    num_unload_stations = 2,
                    sim_duration_hrs = 72,
                    truck_unload_duration = 5,
                    mining_duration_min_hrs = 1,
                    mining_duration_max_hrs = 5)
    results.append(sim_1.run())


average = sum(results)/len(results)

logger.info(f"On average this configuration results in {average} loads.")