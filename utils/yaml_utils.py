import yaml

def getYaml(path: str):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

class Yaml():
    
    def __init__(self, path):
        self.path: str = path
        self.config: yaml._ReadStream = None
        
    
    def loadConfig(self):
        with open(self.path, 'r') as file:
            self.config = yaml.safe_load(file)
    
    def set(self, key, value):
        self.config[key] = value
    
    def get(self, key):
        return self.config[key]

    def save(self):
        with open(self.path, 'w') as file:
            yaml.dump(self.config, file, sort_keys=False)