import numpy
import random


class Game():
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
        
    def game_cheat(self):
        random.shuffle(self.dec52)
        if self.count == 2:
            self.player1_dec, self.player2_dec = numpy.array_split(self.dec52, 2)
        elif self.count == 3:
            self.player1_dec, self.player2_dec, self.player3_dec = numpy.array_split(self.dec52, 3)
        else:
            self.player1_dec, self.player2_dec, self.player3_dec, self.player4_dec = numpy.array_split(self.dec52, 4)
        return