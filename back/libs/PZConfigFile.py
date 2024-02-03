class PZConfigFile:
    def __init__(self, file_name):
        self.file_name = file_name
        self.config = {}
        self.read_file()

    def read_file(self):
        with open(self.file_name, 'r') as file:
            for line in file:
                line = line.strip().replace('\n', '')
                # Ignore commented lines
                if line and not line.startswith('#'):
                    key_value_pair = line.split('=', 1)
                    if len(key_value_pair) == 2:
                        key, value = key_value_pair
                        self.config[key.strip()] = value.strip()

    def get_value(self, key) -> str:
        return self.config.get(key)

    def modify_value(self, key, new_value):
        if key in self.config:
            self.config[key] = new_value
            self.write_file()

    def write_file(self):
        with open(self.file_name, 'w') as file:
            for key, value in self.config.items():
                file.write(f"{key}={value}\n")
