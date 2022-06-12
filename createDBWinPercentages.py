# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 17:12:45 2022

@author: hungd
"""

#%% Libraries

import sqlite3
from sqlite3 import Error
import pandas as pd
import random
from handValue import evaluateHand

#%% Create DB

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    print('Win Percent DB Created')

#%% Create Win Percentage Table
   
def createWinPercentTable(pokerDB):
    # Connect Object
    conn = sqlite3.connect(pokerDB)
    
    # Cursor Object
    curs = conn.cursor()
    
    # Drop the preflopProbs table if already exists
    curs.execute("DROP TABLE IF EXISTS preflopProbs")
    
    # Creating table
    table = """ CREATE TABLE preflopProbs (
                pocket1 INT,
                pocket2 INT,
                players2 REAL,
                players3 REAL,
                players4 REAL,
                players5 REAL,
                players6 REAL,
                players7 REAL,
                players8 REAL,
                players9 REAL,
                players10 REAL
            ); """
    
    # Execute
    curs.execute(table)
    
    # Close the connection
    conn.close()
    print('preflopProbs table created')
    
#%% Card Dict

def writeCardDictToDB(cardDict, pokerDB):
    # Read card dict
    df_cardDict = pd.read_csv(cardDict)
    
    # Write card dict to DB
    conn = sqlite3.connect(pokerDB)
    df_cardDict.to_sql('cardDict', con=conn, if_exists='replace', index=False)
    conn.close()

#%% Win percentage for preflop

def getWinPercentagePreflop(pokerDB, numSim):
    # Create SQL connection
    conn = sqlite3.connect(pokerDB)
    
    # Get Card Dictionary
    sql = """SELECT * FROM cardDict"""
    df_cardDict = pd.read_sql(sql, con=conn)
    
    # Get all possible values preflop
    pocket1List = []
    pocket2List = []
    for i in range(1, 52):
        for j in range(i+1, 53):
            pocket1List.append(i)
            pocket2List.append(j)
    
    # Create df for preflop probs
    df_preflopProbs = pd.DataFrame(columns=['pocket1', 'pocket2'])
    for i in range(2, 11):
        df_preflopProbs['players{}'.format(i)] = 0
    
    # All preflop hands
    for i in range(len(pocket1List)):
        print(i)
        # Define pocket 1 and pocket 2
        pocket1 = pocket1List[i]
        pocket2 = pocket2List[i]
        
        # Create numWins dictionary
        numWins = {}
        for j in range(2, 11):
            numWins['players{}'.format(j)] = 0
        
        # Simulate numSim times
        for j in range(numSim):
            simulatePreflopWin(pocket1, pocket2, df_cardDict, numWins)
            
        # Add pocket cards to numWins dict and append to df_preflopProbs
        numWins['pocket1'] = pocket1
        numWins['pocket2'] = pocket2
        df_numWins = pd.DataFrame([numWins])
        df_preflopProbs = pd.concat([df_preflopProbs, df_numWins])
        
    conn.close()
    
# Simulate preflop win
def simulatePreflopWin(pocket1, pocket2, df_cardDict, numWins):
    # Create a list of remaining cards
    remainingCards = list(range(1,53))
    
    # Remove pocket cards from list
    remainingCards.remove(pocket1)
    remainingCards.remove(pocket2)
    
    # Sample 5 cards to represent board cards
    boardCards = random.sample(remainingCards, 5)
    for card in boardCards:
        remainingCards.remove(card)
        
    # My Score
    myScore = getHighestScoreFrom7Cards(pocket1, pocket2, boardCards, df_cardDict)
    
    # Other Players
    for key in numWins:
        player = random.sample(remainingCards, 2)
        remainingCards.remove(player[0])
        remainingCards.remove(player[1])
        playerScore = getHighestScoreFrom7Cards(player[0], player[1], boardCards, df_cardDict)
        
        if myScore > playerScore:
            numWins[key] += 1
        else:
            break  # For example, if I lose against 3 players, I lose against 10 players
        
# Get highest score from 7 cards
def getHighestScoreFrom7Cards(pocket1, pocket2, boardCards, df_cardDict):
    sevenCards = boardCards[:]
    sevenCards.append(pocket1)
    sevenCards.append(pocket2)
    highestScore = 0
    for i in range(len(sevenCards)-4):
        for j in range(i+1, len(sevenCards)-3):
            for k in range(j+1, len(sevenCards)-2):
                for l in range(k+1, len(sevenCards)-1):
                    for m in range(l+1, len(sevenCards)):
                        values = [df_cardDict['value'].iloc[sevenCards[i]-1],
                                  df_cardDict['value'].iloc[sevenCards[j]-1],
                                  df_cardDict['value'].iloc[sevenCards[k]-1],
                                  df_cardDict['value'].iloc[sevenCards[l]-1],
                                  df_cardDict['value'].iloc[sevenCards[m]-1]]
                        suits = [df_cardDict['suit'].iloc[sevenCards[i]-1],
                                 df_cardDict['suit'].iloc[sevenCards[j]-1],
                                 df_cardDict['suit'].iloc[sevenCards[k]-1],
                                 df_cardDict['suit'].iloc[sevenCards[l]-1],
                                 df_cardDict['suit'].iloc[sevenCards[m]-1]]
                        handScore = evaluateHand(values, suits)
                        highestScore = max(highestScore, handScore)
    return highestScore
        
#%% Main

if __name__ == '__main__':
    # Variables
    pokerDB = 'db/pokerDB.db'
    cardDict = 'db/cardDict.csv'
    numSim = 100
    
    # Create DB
    create_connection(pokerDB)
    
    # Create Card Dictionary
    writeCardDictToDB(cardDict, pokerDB)
    
    # Create preflopProbs table
    createWinPercentTable(pokerDB)
