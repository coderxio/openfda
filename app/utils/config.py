#!/usr/bin/env python
"""apps.utils.config: imports and finalize config.yml"""

from pathlib import Path
import glob
import yaml
import os

class PyVar(yaml.YAMLObject):
    """
    a class to create a custom !PY tag in yaml
    The !PY tag allows calling python code stored in a dictionary
    """
    # this is a PYYAML requirment and is case sensitive
    yaml_tag = u'!PY'

    def __init__(self):
        """
        starts with empty dictionary
        """
        self.py_dict = {}

    def get(self,key):
        """
        retrieves a value from the dictionary
        """
        return self.py_dict[key]

    def add(self,key,value):
        """
        adds a new key value pair to a dictionary
        """
        self.py_dict[key] = value


# construct all they key value pairs that can be referenced by the yaml file
# creating a function like this is required for yaml.SafeLoader.add_constructor
def yaml_construct(loader,node):
    c = PyVar()
    ## start adding python variables here
    c.add('base_dir',Path(__file__).resolve(strict=True).parent.parent.parent.absolute())
    c.add('app_dir', c.get('base_dir') / 'app')
    c.add('data_dir', c.get('app_dir') / 'data')
    c.add('log_dir', c.get('app_dir') / 'log')
    c.add('json_file_name',os.path.basename(max(glob.glob(str(c.get('data_dir')) + '/*.json'), key=os.path.getctime)))
    return c.get(node.value)

# Required for safe_load
yaml.SafeLoader.add_constructor('!PY', yaml_construct)

# config.yml location
configyml_path = Path(__file__).resolve(strict=True).parent.parent.absolute() / "config.yml"

# load config.yml
config = yaml.safe_load(open(configyml_path))

if __name__ == "__main__":
    print(config)