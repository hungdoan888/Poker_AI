# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 19:29:00 2022

@author: hungd
"""

#%% Libraries

import pandas as pd

#%% For Testing

values = ['A', '2', '3', '4', '5']
suits = ['d', 'd', 's', 'd', 'd']

# values = input('Enter Card Values: ')
# suits = input('Enter Suit Values: ')

# values = list(values.strip().split(' '))
# suits = list(suits.strip().split(' '))

#%% Create Ranking Class

class Ranking:
    def __init__(self):
        self.royalFlush = False
        self.straightFlush = False
        self.fourKind = False
        self.fullHouse = False
        self.flush = False
        self.straight = False
        self.threeKind = False
        self.twoPair = False
        self.pair = False
        self.highCard = False

        self.highCardValue1 = 0
        self.highCardValue2 = 0
        self.highCardValue3 = 0
        self.highCardValue4 = 0
        self.highCardValue5 = 0
        self.pairValue1 = 0
        self.pairValue2 = 0
        self.threeKindValue = 0
        self.fourKindValue = 0
        self.straightHighCardValue2 = 0
        self.flushHighCardValue = 0

        self.handValue = 0

#%% Create Hand df

def createHandDf(values, suits):
    # Get Numeric Values
    numValues = convertValueToNumValue(values)

    # Create df
    hand = pd.DataFrame({'value': values, 'suit': suits, 'numValue': numValues})
    
    # Sort Values
    hand = hand.sort_values('numValue').reset_index(drop=True)
    return hand

# Convert value to numeric value
def convertValueToNumValue(values):
    numericDict = {'2': 2, 
                   '3': 3, 
                   '4': 4,
                   '5': 5,
                   '6': 6,
                   '7': 7,
                   '8': 8,
                   '9': 9,
                   '10': 10,
                   'J': 11,
                   'Q': 12,
                   'K': 13,
                   'A': 14}
    numValues = []
    for value in values:
        numValues.append(numericDict[value])
    return numValues

#%% Determine Hand

# Straight
def isStraight(hand, ranking):
    if (hand['value'].iloc[0] == '2' and
        hand['value'].iloc[1] == '3' and 
        hand['value'].iloc[2] == '4' and 
        hand['value'].iloc[3] == '5' and 
        hand['value'].iloc[4] == 'A'):
        ranking.straight = True
        ranking.straightHighCardValue2 = hand['numValue'].iloc[3]
        return

    uniqueDiffs = hand['numValue'].diff().drop_duplicates().dropna()
    if uniqueDiffs.count() == 1 and uniqueDiffs.iloc[0] == 1:
        ranking.straight = True
        ranking.straightHighCardValue2 = hand['numValue'].iloc[3]

# Flush
def isFlush(hand, ranking):
    uniqueSuitsCount = hand['suit'].drop_duplicates().count()
    if uniqueSuitsCount == 1:
        ranking.flush = True
        ranking.flushHighCardValue = hand['numValue'].max()

# Straight Flush
def isStraightFlush(ranking):
    ranking.straightFlush = ranking.straight and ranking.flush

# Royal Flush
def isRoyalFlush(hand, ranking):
    if not ranking.straightFlush:
        return

    # Determine if straight flush starts with an Ace
    ranking.royalFlush = hand['numValue'].max() == 14

# Pair, Two pair, Three of a kind, full house, four of a kind
def pairings(hand, ranking):
    handPairs = (hand.groupby(['value', 'numValue'])['numValue']
                     .count()
                     .to_frame('count')
                     .sort_values(['count', 'numValue'], ascending=False)
                     .reset_index())

    # No Pairs
    if len(handPairs) == 5:
        ranking.highCard = True
        ranking.highCardValue1 = handPairs['numValue'].iloc[0]
        ranking.highCardValue2 = handPairs['numValue'].iloc[1]
        ranking.highCardValue3 = handPairs['numValue'].iloc[2]
        ranking.highCardValue4 = handPairs['numValue'].iloc[3]
        ranking.highCardValue5 = handPairs['numValue'].iloc[4]

    # Pair
    elif len(handPairs) == 4:
        ranking.pair = True
        ranking.pairValue1 = handPairs['numValue'].iloc[0]
        ranking.highCardValue1 = handPairs['numValue'].iloc[1]
        ranking.highCardValue2 = handPairs['numValue'].iloc[2]
        ranking.highCardValue3 = handPairs['numValue'].iloc[3]

    # Two Pair
    elif len(handPairs) == 3 and handPairs['count'].max() == 2:
        ranking.twoPair = True
        ranking.pairValue1 = handPairs['numValue'].iloc[0]
        ranking.pairValue2 = handPairs['numValue'].iloc[1]
        ranking.highCardValue1 = handPairs['numValue'].iloc[2]

    # Three of a Kind
    elif len(handPairs) == 3 and handPairs['count'].max() == 3:
        ranking.threeKind = True
        ranking.threeKindValue = handPairs['numValue'].iloc[0]
        ranking.highCardValue1 = handPairs['numValue'].iloc[1]
        ranking.highCardValue2 = handPairs['numValue'].iloc[2]

    # Full House
    elif len(handPairs) == 2 and handPairs['count'].max() == 3:
        ranking.fullHouse = True
        ranking.threeKindValue = handPairs['numValue'].iloc[0]
        ranking.pairValue1 = handPairs['numValue'].iloc[1]

    # Four of a kind
    elif len(handPairs) == 2 and handPairs['count'].max() == 4:
        ranking.fourKind = True
        ranking.fourKindValue = handPairs['numValue'].iloc[0]
        ranking.highCardValue1 = handPairs['numValue'].iloc[1]

    else:
        print('Error when evaluating pairs')   

#%% Evaluate Hand

def evaluateHand(ranking):
    # Royal Flush
    if ranking.royalFlush:
        ranking.handValue = 10
        print('Royal Flush')

    # Straight Flush
    elif ranking.straightFlush:
        ranking.handValue = 9
        ranking.handValue += (ranking.straightHighCardValue2 * .01)
        print('Straight Flush')

    # Four of a kind
    elif ranking.fourKind:
        ranking.handValue = 8
        ranking.handValue += (ranking.fourKindValue * .01 + ranking.highCardValue1 * .0001)
        print('Four of a kind')

    # Full House
    elif ranking.fullHouse:
        ranking.handValue = 7
        ranking.handValue += (ranking.threeKindValue * .01 + ranking.pairValue1 * .0001)
        print('Full House')

    # Flush
    elif ranking.flush:
        ranking.handValue = 6
        ranking.handValue += (ranking.flushHighCardValue * .01)
        print('Flush')

    # Straight
    elif ranking.straight:
        ranking.handValue = 5
        ranking.handValue += (ranking.straightHighCardValue2 * .01)
        print('Straight')

    # Three of a kind
    elif ranking.threeKind:
        ranking.handValue = 4
        ranking.handValue += (ranking.threeKindValue * .01 + 
                              ranking.highCardValue1 * .0001 + 
                              ranking.highCardValue2 * .000001)
        print('Three of a kind')

    # Two Pair
    elif ranking.twoPair:
        ranking.handValue = 3
        ranking.handValue += (ranking.pairValue1 * .01 + 
                              ranking.pairValue2 * .0001 + 
                              ranking.highCardValue1 * .000001)
        print('Two Pair')

    # Pair
    elif ranking.pair:
        ranking.handValue = 2
        ranking.handValue += (ranking.pairValue1 * .01 + 
                              ranking.highCardValue1 * .0001 + 
                              ranking.highCardValue2 * .000001 + 
                              ranking.highCardValue3 * .00000001)
        print('Pair')

    # High Card
    elif ranking.highCard:
        ranking.handValue = 1
        ranking.handValue += (ranking.highCardValue1 * .01 + 
                              ranking.highCardValue2 * .0001 + 
                              ranking.highCardValue3 * .000001 + 
                              ranking.highCardValue4 * .00000001 + 
                              ranking.highCardValue5 * .0000000001)
        print('High Card')
    print(ranking.handValue)

#%% Main

# Define Ranking
ranking = Ranking()

# Create Hand
hand = createHandDf(values, suits)

# Determine Straight
isStraight(hand, ranking)
isFlush(hand, ranking)
isStraightFlush(ranking)
isRoyalFlush(hand, ranking)
pairings(hand, ranking)
evaluateHand(ranking)

# %%
