from mcrcon import MCRcon


class PZRcon:
    possible_decodings = ['utf-8', 'latin-1', 'ascii', 'cp1252']

    def __init__(self, rcon_host: str, rcon_port: str, rcon_password: str):
        self.rcon_host = rcon_host
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password

    def check_open(self):
        try:
            with MCRcon(self.rcon_host, port=int(self.rcon_port), password=self.rcon_password) as client:
                client.connect()
                return True
        except Exception as e:
            print(e)
            return False

    async def send_command(self, cmd: str):
        try:
            with MCRcon(self.rcon_host, port=int(self.rcon_port), password=self.rcon_password) as client:
                result = client.command(cmd)
                print(result)
                client.disconnect()
                return result
        except UnicodeDecodeError as erreur_unicode:
            content = erreur_unicode.args[1]
            for decoding in self.possible_decodings:
                try:
                    text = content.decode(decoding)
                    print(f'decoding with {decoding}')
                    return text
                except UnicodeDecodeError:
                    # If a decoding error occurs, move to the next decoding
                    continue
            return False
        except Exception as e:
            print(e)
            return False
