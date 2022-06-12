# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 10:37:10 2022

@author: hungd
"""

#%% Libraries

import sqlite3
import pandas as pd
from handValue import evaluateHand

#%% Create seven cards score table
   
def sevenCardsScoreTable(pokerDB):
    # Connect Object
    conn = sqlite3.connect(pokerDB)
    
    # Cursor Object
    curs = conn.cursor()
    
    # Drop the preflopProbs table if already exists
    curs.execute("DROP TABLE IF EXISTS sevenCardsScore")
    
    # Creating table
    table = """ CREATE TABLE sevenCardsScore (
                key INT,
                pocket1 INT,
                pocket2 INT,
                flop1 INT,
                flop2 INT,
                flop3 INT,
                turn INT,
                river INT,
                score REAL
            ); """
    
    # Execute
    curs.execute(table)
    
    # Close the connection
    conn.close()
    print('sevenCardsScore table created')
    
#%% Get Card Dictionary

def getCardDict(pokerDB):
    # Create SQL connection
    conn = sqlite3.connect(pokerDB)
    
    # Get Card Dictionary
    sql = """SELECT * FROM cardDict"""
    df_cardDict = pd.read_sql(sql, con=conn)
    return df_cardDict

#%% Get highest score from 7 cards

def getHighestScoreFrom7Cards(sevenCards, df_cardDict):             
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

#%% Get seven card scores

def getSevenCardScores(df_cardDict, pokerDB):
    # Create SQL connection
    conn = sqlite3.connect(pokerDB)
    cur = conn.cursor()
    sql = ''' INSERT INTO sevenCardsScore(key, pocket1, pocket2, flop1, flop2, flop3, turn, river,
                                          score)
              VALUES(?,?,?,?,?,?,?,?,?)'''
              
    keyCount = 1
    for i in range(1, 47):
        for j in range(i+1, 48):
            for k in range(j+1, 49):
                for l in range(k+1, 50):
                    for m in range(l+1, 51):
                        for n in range(m+1, 52):
                            for o in range(n+1, 53):
                                if keyCount % 1000 == 0:
                                    conn.commit()
                                    print(keyCount)
                                sevenCards = [i, j, k, l, m, n, o]
                                handScore = getHighestScoreFrom7Cards(sevenCards, df_cardDict)
                                sqlValues = (keyCount, i, j, k, l, m, n, o, handScore)
                                cur.execute(sql, sqlValues)
                                keyCount += 1
    conn.commit()
    conn.close()
                                
#%% Main

if __name__ == '__main__':
    # Variables
    pokerDB = 'db/pokerDB.db'
    
    # Create seven cards score table
    sevenCardsScoreTable(pokerDB)
    
    # Get Card Dict
    df_cardDict = getCardDict(pokerDB)

    # Get seven card scores
    getSevenCardScores(df_cardDict, pokerDB)