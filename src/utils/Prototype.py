import logging

class Prototype:
    """
        Parent abstract class in which all modules inherit from
        Defines logging and some other configuration
    """
    
    def __init__(self) -> None:
        logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.INFO)
        self.logger = logging.getLogger('content-generation')
