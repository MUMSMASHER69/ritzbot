import discord
import re
import json
import random
from random import shuffle
import logging
import logging.config
import requests
import yfinance as yf

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

        if ("!crypto" in message.content.lower()):
            if ("all" in message.content.lower()):
                markets = ["BTC-AUD", "LTC-AUD", "ETH-AUD", "XRP-AUD"]
                sendStr = ""
                for i in markets:
                    r = requests.get('https://api.btcmarkets.net/v3/markets/{}/ticker'.format(i))
                    rjson = r.json()
                    sendStr += "{} price: ${} \nAsk: ${} \nBid: ${} \n24h low: ${} \n24h high: ${} \n24h change: {}% \n\n".format(i.split("-")[0] ,rjson["lastPrice"], rjson["bestAsk"], rjson["bestBid"], rjson["low24h"], rjson["high24h"], rjson["pricePct24h"])
                await message.channel.send(sendStr)
                return
            if ("btc" in message.content.lower()):
                r = requests.get('https://api.btcmarkets.net/v3/markets/BTC-AUD/ticker')
                rjson = r.json()
            elif ("ltc" in message.content.lower()):
                r = requests.get('https://api.btcmarkets.net/v3/markets/LTC-AUD/ticker')
                rjson = r.json()
            elif ("eth" in message.content.lower()):
                r = requests.get('https://api.btcmarkets.net/v3/markets/ETH-AUD/ticker')
                rjson = r.json()
            elif ("xrp" in message.content.lower()):
                r = requests.get('https://api.btcmarkets.net/v3/markets/XRP-AUD/ticker')
                rjson = r.json()
            else:
                await message.channel.send("Example command is !crypto btc. Possible markets are btc, ltc, xrp and eth")
                return

            await message.channel.send("{} price: ${} \nAsk: ${} \nBid: ${} \n24h low: ${} \n24h high: ${} \n24h change: {}".format(rjson["marketId"], rjson["lastPrice"], rjson["bestAsk"], rjson["bestBid"], rjson["low24h"], rjson["high24h"], rjson["pricePct24h"]))
            return

        if (message.content.lower().startswith("!asx")):
            try:
                ticker = yf.Ticker(message.content.lower().split(" ")[1].upper() + ".AX")
                marketInfo = ticker.info
                daychange = (float(marketInfo["dayHigh"]) - float(marketInfo["dayLow"])) / abs(marketInfo["dayLow"])
                sendStr = "Prices in {}\n{} price: ${:.2f} \nAsk: ${:.2f} \nBid: ${:.2f} \n24h low: ${:.2f} \n24h high: ${:.2f} \n24h change: {:.2%} \n\n".format(marketInfo["currency"], marketInfo["longName"], marketInfo["bid"], marketInfo["ask"], marketInfo["bid"], marketInfo["dayLow"], marketInfo["dayHigh"], daychange)
                await message.channel.send(sendStr)
                return
            except:
                await message.channel.send("Example command is !asx CBA. Possible markets are all in the ASX")
                return

        if (message.content.lower().startswith("!stocks")):
            try:
                ticker = yf.Ticker(message.content.lower().split(" ")[1].upper())
                marketInfo = ticker.info
                if (marketInfo["bid"] == 0 and marketInfo["ask"] == 0):
                    marketHistory = ticker.history('1d').to_dict(orient="records")[0]
                    daychange = (float(marketHistory["High"]) - float(marketHistory["Low"])) / abs(marketHistory["Low"])
                    sendStr = "Market closed.\nPrices in {}\n{}\nClose: ${:.2f} \nOpen: ${:.2f}\n24h low: ${:.2f} \n24h high: ${:.2f} \n24h change: {:.2%} \n\n".format(marketInfo["currency"],marketInfo["longName"], marketHistory["Close"], marketHistory["Open"], marketHistory["Low"], marketHistory["High"], daychange)
                else:    
                    daychange = (float(marketInfo["dayHigh"]) - float(marketInfo["dayLow"])) / abs(marketInfo["dayLow"])
                    sendStr = "Prices in {}\n{} price: ${:.2f} \nAsk: ${:.2f} \nBid: ${:.2f} \n24h low: ${:.2f} \n24h high: ${:.2f} \n24h change: {:.2%} \n\n".format(marketInfo["currency"], marketInfo["longName"], marketInfo["bid"], marketInfo["ask"], marketInfo["bid"], marketInfo["dayLow"], marketInfo["dayHigh"], daychange)
                await message.channel.send(sendStr)
                return
            except Exception as e:
                logger.error(e, exc_info=True)
                await message.channel.send("Example command is !stocks TSLA. Ensure that you type the correct stock code")

                return

        # random
        rare_num = random.randint(0,100)
        epic_num = random.randint(0, 1000)
        legendary_num = random.randint(0, 10000)
        based = random.randint(0,100000)
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
        elif (based == 69):
            logger.info("based")

        # darren
        if (str(message.author) == "mckhira#3664"):
            if ("no u" in message.content.lower()):
                await message.channel.send("Darren is gay")
                return
            else:
                num = random.randint(0,20)
                if (num == 1):
                    await message.channel.send("Darren is gay")
                    return
                
        if (str(message.author) == "cookedswag#5260"):
            swag_num = random.randint(0,10)
            if (swag_num == 1):
                await message.channel.send("The man has spoken.")
            elif (swag_num == 2):
                message.channel.send("The boss has spoken.")
            elif (swag_num == 3):
                await message.channel.send("The legend has spoken.")
            return

def main():
    client = MyClient()
    client.run(tokenfile["token"])


if __name__ == "__main__":
    main()
