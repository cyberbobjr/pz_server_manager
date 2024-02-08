global pzDiscord


class PZLog:

    @staticmethod
    async def print(msg: str):
        from main import pzDiscord
        try:
            if pzDiscord:
                await pzDiscord.send_message(msg)
        finally:
            print(msg)
