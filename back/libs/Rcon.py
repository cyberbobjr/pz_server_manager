from mcrcon import MCRcon


class PZRcon:
    def __init__(self, rcon_host: str, rcon_port: str, rcon_password: str):
        self.rcon_host = rcon_host
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password

    def check_open(self):
        try:
            with MCRcon(self.rcon_host, port=self.rcon_port, password=self.rcon_password) as client:
                # await client.connect()
                # result = client.command(cmd)
                # print(result)
                # await client.close()
                # return result
                return True
        except Exception as e:
            print(e)
            return False
