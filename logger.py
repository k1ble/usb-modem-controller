import logging
from logging.handlers import RotatingFileHandler
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
      "logger.log",     
      maxBytes = 1024 * 1024,
      backupCount = 1 
)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S"
                              )

handler.setFormatter(formatter) #formatter chain
logger.addHandler(handler) #handler chain

