import logging
    
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler(f'{__name__}.log', mode = "a")

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S"
                              )

handler.setFormatter(formatter) #formatter chain
logger.addHandler(handler) #handler chain

