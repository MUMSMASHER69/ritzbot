import numpy as np
import random
import logging
import logging.config

from os import path
logging.config.fileConfig(
    path.join(path.dirname(path.abspath(__file__)), "config/logger.ini"), disable_existing_loggers=False
)
logger = logging.getLogger(__name__)

class Cheat():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.player3 = ""
        self.player4 = ""
        self.players = []
        self.strplayers = []
        self.player1_dec = []
        self.player2_dec = []
        self.player3_dec = []
        self.player4_dec = []
        self.hands = []
        self.count = 0
        self.gamestatus = False
        self.playerturn = ""
        self.playerturncount = 0
        
        self.suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
        self.cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        
        self.dec52 = []

        for suit in self.suits:
            for card in self.cards:
                self.dec52.append(card + " of " + suit)
        return
        
    def shuffle_deck(self):
        random.shuffle(self.dec52)
        if self.count == 2:
            self.player1_dec, self.player2_dec = np.array_split(self.dec52, 2)
        elif self.count == 3:
            self.player1_dec, self.player2_dec, self.player3_dec = np.array_split(self.dec52, 3)
        else:
            self.player1_dec, self.player2_dec, self.player3_dec, self.player4_dec = np.array_split(self.dec52, 4)
        return

    async def init_game(self, message):
        logger.debug("init game")
        self.player1 = message.author
        self.players.append(self.player1)
        logger.debug(self.player1)
        await message.channel.send(str(self.player1) + " started a lobby of cheat.")
        self.count += 1
        logger.debug(self.count)
        return

    
    async def join(self, message):
        logger.debug("join game")
        if self.count == 0:
            await message.channel.send("Game has not been started yet, perform !play cheat to start a game")
        elif self.count == 1:
            self.player2 = message.author
            # self.players.append(self.player2)
            # self.strplayers.append(str(self.player2))
            self.count += 1
            await message.channel.send(str(self.player2) + " has joined the lobby game of cheat 2/4")
        elif self.count == 2:
            self.player3 = message.author
            # self.players.append(self.player3)
            # self.strplayers.append(str(self.player3))
            self.count += 1
            await message.channel.send(str(self.player3) + " has joined the lobby game of cheat 3/4")
        elif self.count == 3:
            self.player4 = message.author
            # self.players.append(self.player4)
            # self.strplayers.append(str(self.player4))
            self.count += 1
            await message.channel.send(str(self.player4) + " has joined the lobby game of cheat 4/4")
        else:
            await message.channel.send("Full Lobby 4/4 with {}, {}, {}, {}".format(str(self.player1), str(self.player2), str(self.player3), str(self.player4)))
        return

    async def start(self, message):
        logger.debug("start game")
        await message.channel.send("Starting a game of BULLSHIT with " + str(self.count) + " players!")
        self.gamestatus = True
        # shuffle deck and split for players
        self.shuffle_deck()
        
        # add players to player list
        self.players.append(self.player1)
        self.players.append(self.player2) 
        self.players.append(self.player3)
        self.players.append(self.player4)
        
        # add player name string to player string list
        self.strplayers.append(str(self.player1))
        self.strplayers.append(str(self.player2)) 
        self.strplayers.append(str(self.player3))
        self.strplayers.append(str(self.player4))
        
        # add player hands to hands list
        self.hands.append(self.player1_dec)
        self.hands.append(self.player2_dec)
        self.hands.append(self.player3_dec)
        self.hands.append(self.player4_dec)

        logger.info(self.strplayers)
        for i in range(4-self.count):
            self.players.pop()
            self.strplayers.pop()
            # self.hands.pop()
        logger.info(self.strplayers)
        
        # dm each player their hand
        for player in range(0, self.count):
            await self.players[player].send(self.hands[player])
            
        # set whose turn it is
        self.playerturn = self.players[self.playerturncount]

        # dm player that it is their turn
        await self.playerturn.send("It is your turn")

        # send message to everyone with whose turn it is
        await message.channel.send(str(self.playerturn) + "'s turn!")

        # next turn
        self.playerturncount += 1
        return

    async def gameplayLoop(self, message):
        logger.debug("gameplay loop")
        if ((str(message.author) in self.strplayers) and self.gamestatus):
            if str(message.author) == str(self.playerturn):
                logger.info(self.playerturncount)
                self.playerturn = self.strplayers[self.playerturncount]
                # self.playerturn = self.players[self.playerturncount]
                
                # self.dm_all(message.content.lower(), self.players)
                await message.channel.send(message.content.lower())
                
                # self.dm_all(self.playerturn + "'s turn!", self.players)
                await message.channel.send(self.playerturn + "'s turn!")
                logger.info(self.players)
                
                self.playerturncount += 1
                if self.playerturncount == self.count:
                    self.playerturncount = 0
                    self.playerturn = self.strplayers[self.playerturncount]
            else:
                await message.author.send("Not your turn")
            return

    def leave(self, player):
        logger.debug("leave game")


