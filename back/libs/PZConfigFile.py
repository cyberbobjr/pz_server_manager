import re


class PZConfigFile:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_content(self):
        with open(self.file_name, 'r') as file:
            return file.read()

    def put_content(self, content):
        with open(self.file_name, 'w') as file:
            file.write(content)
        return self.get_content()

    def get_value(self, key) -> str:
        pattern = rf'\s*{re.escape(key.strip())}\s*=\s*(.*)'
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                match = re.match(pattern, line)
                if match:
                    return match.group(1)

    def write_value(self, key, value):
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if re.match(rf'\s*{key.strip()}\s*=', line):
                    new_line = f"{key.strip()}=" + str(value) + "\n"
                    lines[i] = new_line

        with open(self.file_name, 'w') as file:
            file.writelines(lines)

        return lines
