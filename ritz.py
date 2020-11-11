import discord
import re
import json
import random

with open("config/config.json", 'r') as f:
    config = json.load(f)

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

        # dollar to ritz conversion
        for i in searchList:
            found = re.search(i, message.content)
            if (found):
                ritzAmount = float(found.group(1)) / ritzprice
                if (ritzAmount.is_integer()):
                    ritzAmount = int(ritzAmount)
                ritzString = "{} Ritz".format(ritzAmount)
                await message.channel.send(str(ritzString), file=discord.File("./images/ritz.jpeg"))
                return

        # word responses
        for i in config["words"]:
            if (i["word"] in message.content.lower()):
                if (i["type"] == "link"):
                    await message.channel.send(random.choice(i["content"]))
                    return
                elif (i["type"] == "image"):
                    await message.channel.send(file=discord.File(random.choice(i["content"])))
                    return

        if ("!help" == message.content.lower()):
            words = ""
            for i in config["words"]:
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
        super_rare_num = random.randint(0, 1000)
        ultra_rare_num = random.randint(0, 10000)
        if (ultra_rare_num == 69):
            print("ultra rare")
            choice = config["ultra_rare"]
            await message.channel.send(file=discord.File("./images/" + random.choice(choice)))
            return
        elif (super_rare_num == 69):
            print("super rare")
            choice = config["super_rare"]
            await message.channel.send(file=discord.File("./images/" + random.choice(choice)))
            return
        elif (rare_num == 69):
            print('yo')
            choice = config["rare"]
            await message.channel.send(file=discord.File("./images/" + random.choice(choice)))
            return

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
    client.run(config["token"])


if __name__ == "__main__":
    main()