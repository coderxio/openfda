#!/usr/bin/env python
"""apps.utils.config: imports and finalize config.yml"""

from pathlib import Path
import re
import glob
import os

# third-party
import yaml

class Config:
    """
    a class that:
    1) loads yml file on initialization
    2) allows injecting python code to the config dictionary
    3) replaces yml references with their values
    """
    def __init__(self,value=Path(__file__).resolve(strict=True).parent.parent.absolute() / "config.yml"):
        # config.yml location
        self.yml_config_path = value
        self.configs = {}
        self.load_yaml()

    def load_yaml(self):
        """
        puts config.yml content in a dictionary
        """
        self.configs = yaml.safe_load(open(self.yml_config_path))

    def replace_dynamic(self,key,new_value):
        """
        replace any mention of <dynamic> for the key specificed with a new value
        """
        self.configs[key] = new_value if self.configs[key] == '<dynamic>' else self.configs[key]

    def replace_references(self):
        """
        replace any mention of <variable> with its value
        """
        # loop through each key value pair and replace <refernces> with their values.
        for key, value in self.configs.items():
            if isinstance(value, str):
                vars_to_replace = re.findall(r'(?=\<[A-z]+\>)(?!\<dynamic\>)([A-z><]+)',value)
                for var in vars_to_replace:
                    if isinstance(self.configs[var[1:-1]], Path):
                        self.configs[key] = Path(value.replace(var,str(self.configs[var[1:-1]])))
                        # make directories if they do not exist
                        Path(value.replace(var,str(self.configs[var[1:-1]]))).mkdir(parents=True, exist_ok=True)
                    else:
                        self.configs[key] = value.replace(var,self.configs[var[1:-1]])

    def get(self,key):
        """
        return the value for they key requested
        """
        return self.configs[key]

    def all(self):
        """
        returns all configs
        """
        return self.configs

# initiate config
config = Config()
# get the realtive path and assign it to base_dir
config.replace_dynamic('base_dir',Path(__file__).resolve(strict=True).parent.parent.parent.absolute())
# subsitute all references with their values
config.replace_references()
# get the latest json file
config.replace_dynamic('json_file_name',os.path.basename(max(glob.glob(str(config.get('data_dir')) + '/*.json'), key=os.path.getctime)))


if __name__ == "__main__":
    print(config.all())
else:
    config = config.all()