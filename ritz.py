import discord
import re
import json
import random
from random import shuffle
import logging
import logging.config

logging.config.fileConfig(
    "./config/logger.ini", disable_existing_loggers=False
)
logger = logging.getLogger(__name__)

with open("config/config.json", 'r') as f:
    config = json.load(f)

with open("config/token.json", 'r') as f:
    tokenfile = json.load(f)
    

searchList = [    
    r"\$(\d+\.?[0-9]?[0-9]?)",
    r"(\d+) [Dd]ollar[s]?",
    r"(\d+) [Bb]uck[s]?"
]
ritzprice = config["ritz_price"]

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        # exit is message is from self
        if (message.author == self.user):
            return

        # if (str(message.author) == "cookedswag#5260"):
        #     return

        # dollar to ritz conversion
        for i in searchList:
            found = re.search(i, message.content)
            if (found):
                ritzAmount = float(found.group(1)) / ritzprice
                if (ritzAmount.is_integer()):
                    ritzAmount = int(ritzAmount)
                ritzString = "{:.2f} Ritz at ${:.2f} per box".format(ritzAmount, ritzprice)
                await message.channel.send(str(ritzString), file=discord.File("./images/ritz.jpeg"))
                return

        # word responses
        wordList = config["words"]
        shuffle(wordList)
        for i in wordList:
            if (i["word"] in message.content.lower()):
                if (i["type"] == "link"):
                    await message.channel.send(random.choice(i["content"]))
                    return
                elif (i["type"] == "image"):
                    await message.channel.send(file=discord.File("./images/" + random.choice(i["content"])))
                    return

        if ("!help" == message.content.lower()):
            words = ""
            wordList = config["words"]
            shuffle(wordList)
            for i in wordList:
                words += "\t" + i["word"] + "\n"

            with open("help.txt", 'r') as f:
                content = f.read().format(words)
                await message.channel.send(content)
            return
        
        if ("!coinflip" == message.content.lower()):
            chance = ["Heads", "Tails"]
            await message.channel.send("vibin'\n" + random.choice(chance))
            return

        # random
        rare_num = random.randint(0,100)
        epic_num = random.randint(0, 1000)
        legendary_num = random.randint(0, 10000)
        if (legendary_num == 69):
            logger.info("Legendary")
            choice = config["legendary"]
            await message.channel.send("Legendary. Just vibin' in the ritz car.", file=discord.File("./images/" + random.choice(choice)))
            return
        elif (epic_num == 69):
            logger.info("Epic")
            choice = config["epic"]
            await message.channel.send("Epic. What.", file=discord.File("./images/" + random.choice(choice)))
            return
        # elif (rare_num == 69):
        #     logger.info("Rare")
        #     choice = config["rare"]
        #     await message.channel.send("Rare.", file=discord.File("./images/" + random.choice(choice)))
        #     return

        # darren
        if (str(message.author) == "mckhira#3664"):
            if ("no u" in message.content.lower()):
                await message.channel.send("Darren is gay", file=discord.File("./images/femboy.jpg"))
                return
            else:
                num = random.randint(0,20)
                if (num == 1):
                    await message.channel.send("Darren is gay", file=discord.File("./images/femboy.jpg"))
                    return

def loadConfig():
    with open("config/config.json", 'r') as f:
        config = json.load(f)
        return config

def main():
    client = MyClient()
    client.run(tokenfile["token"])


if __name__ == "__main__":
    main()