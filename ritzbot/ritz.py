from ritzbot import cheat, helpers, functions
import discord
import random
import logging
import logging.config
from os import path
logging.config.fileConfig(
    path.join(path.dirname(path.abspath(__file__)), "config/logger.ini"), disable_existing_loggers=False
)
logger = logging.getLogger(__name__)

config = helpers.open_config()
tokenfile = helpers.open_token()


class DiscordClient(discord.Client):
    async def on_ready(self):
        logger.debug('Logged on as {0}!'.format(self.user))
        self.cheat = ''

    async def dm_all(self, msg, authors):
        logger.debug(msg)
        for author in authors:
            if author != "":
                await author.send(msg)
        return

    async def on_message(self, message):
        # exit if message is from self
        if (message.author == self.user):
            return

        await functions.dollarToRitz(message)
        await functions.wordSearch(message)

        if ("!help" == message.content.lower()):
            await functions.help(message)

        # coin flip
        if ("!coinflip" == message.content.lower()):
            await functions.coinflip()

        # crypto
        if ("!crypto" in message.content.lower()):
            await functions.crypto(message)

        # asx
        if (message.content.lower().startswith("!asx")):
            await functions.asx(message)

        # stocks
        if (message.content.lower().startswith("!stocks")):
            await functions.stocks(message)

        # random images
        await functions.luckyDip(message)

        # darren
        if (str(message.author) == "mckhira#3664"):
            if ("no u" in message.content.lower()):
                await message.channel.send("Darren is gay")
                return
            else:
                num = random.randint(0, 20)
                if (num == 1):
                    await message.channel.send("Darren is gay")
                    return

        if (str(message.author) == "cookedswag#5260"):
            swag_num = random.randint(0, 10)
            if (swag_num == 1):
                await message.channel.send("The man has spoken.")
            elif (swag_num == 2):
                message.channel.send("The boss has spoken.")
            elif (swag_num == 3):
                await message.channel.send("The legend has spoken.")
            return

        # cheat game
        if (message.content.lower() == "!play cheat"):
            if self.cheat == '':
                self.cheat = cheat.Cheat()
                await self.cheat.init_game(message)
                logger.debug(self.cheat)
            else:
                await message.channel.send("Game is currently running. Perform !join cheat to join the lobby.")
            return

        if (message.content.lower() == "!join cheat"):
            if self.cheat == '':
                await message.channel.send("Game has not been started yet, perform !play cheat to start a game")
            else:
                await self.cheat.join(message)
            return

        if (message.content.lower() == "!start cheat"):
            if self.cheat != '':
                await self.cheat.start(message)
            else:
                await message.channel.send("Not enough players!")
            return
        if (self.cheat != ''):
            await self.cheat.gameplayLoop(message)


def main():
    client = DiscordClient()
    client.run(tokenfile["token"])


if __name__ == "__main__":
    main()
