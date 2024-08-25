import yaml
from src.utils.Prototype import Prototype
import os

class ConfigLoader(Prototype):
    """
    Interface to easily handle configuration import for video text generation
    Loads data as YAML
    Completely stateless
    """
    def __init__(self) -> None:
        super().__init__()
    
    def read(self, filepath: str) -> any:
        """Reads data as a python dict object from a .yaml file

        Args:
            filepath (str): absolute path to the file to be written

        Raises:
            e: OSerror

        Returns:
            Any: A python dict object
        """
        try:
            with open(filepath, "r") as f:
                self.logger.debug("File Successfully Read: " + filepath)
                return yaml.safe_load(f)
        except Exception as e:
            raise e  
        
    def write(self, filepath: str, data: any):
        """Writes data from python object to a .yaml file. 
        Overwrites file
        If file does not exist, creates it

        Args:
            filepath (str): absolute path to the file to be written
            data (any): data to be written as a python object

        Raises:
        e: OSerror

        Returns:
            None
        """

        head, tail = os.path.split(filepath)

        try:
            os.mkdir(head)
        except Exception as e:
            self.logger.warn("Directory " + head + " already exists")

        with open(filepath, "w+", encoding='utf-8') as f:
            f.truncate(0)
            yaml.dump(data, f, allow_unicode=True, indent=4)
            self.logger.debug("File Successfully Written: " + filepath)