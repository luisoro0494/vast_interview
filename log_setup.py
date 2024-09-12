import logging
from datetime import datetime

# Configure the logger
def configure_logger() -> None:
    log_name = datetime.now().strftime("%Y-%m-%d-%H-%M_lunar_helium_3_sim.log")
    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
        handlers=[
            logging.FileHandler(log_name),  # Log to a file
            logging.StreamHandler()  # Log to console
        ]
    )
