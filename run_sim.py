# import yaml
import logging

from simulator import lunar_Helium_3_sim
from log_setup import configure_logger

# Configure the logger
configure_logger()
logger = logging.getLogger(__name__)


sim_1 = lunar_Helium_3_sim(
                num_mining_trucks = 10,
                num_unload_stations = 2,
                sim_duration_hrs = 72,
                truck_unload_duration = 5,
                travel_to_unload = 30,
                mining_duration_min_hrs = 1,
                mining_duration_max_hrs = 5)

# an example of how to run multiple sims and get an average of completed loads
# per configuration.

sim_1.run()
