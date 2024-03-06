class PZLuaFile:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_content(self):
        with open(self.file_name, 'r') as file:
            return file.read()

    def put_content(self, content):
        with open(self.file_name, 'w') as file:
            file.write(content)
        return self.get_content()
