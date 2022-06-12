# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:31:13 2022

@author: hungd
"""

#%% Libraries

import pandas as pd
import math
from handValue import evaluateHand

#%% For Testing

testData = 'data/poker-hand-training-true.data'

#%% Import Test Data

def importTestData(testData):
    # Read Data
    df_test = pd.read_csv(testData, header=None)
    return df_test

#%% Format Test Data

# Format Test Data
def formatTestData(df_test):
    allValues = formatValues(df_test)
    allSuits = formatSuits(df_test)
    scores = formatScores(df_test)
    return allValues, allSuits, scores

# Values
def formatValues(df_test):
    df_values = df_test.loc[:, [1, 3, 5, 7, 9]]
    
    # Replace numbers with letters
    df_values = df_values.replace(1, 'A')
    df_values = df_values.replace(13, 'K')
    df_values = df_values.replace(12, 'Q')
    df_values = df_values.replace(11, 'J')
    df_values = df_values.replace(10, '10')
    df_values = df_values.replace(9, '9')
    df_values = df_values.replace(8, '8')
    df_values = df_values.replace(7, '7')
    df_values = df_values.replace(6, '6')
    df_values = df_values.replace(5, '5')
    df_values = df_values.replace(4, '4')
    df_values = df_values.replace(3, '3')
    df_values = df_values.replace(2, '2')
    
    # Convert values to list
    allValues = df_values.values.tolist()
    return allValues

# Suits
def formatSuits(df_test):
    df_suits = df_test.loc[:, [0, 2, 4, 6, 8]]
    
    # Replace numbers with letters
    df_suits = df_suits.replace(1, 'h')
    df_suits = df_suits.replace(2, 's')
    df_suits = df_suits.replace(3, 'd')
    df_suits = df_suits.replace(4, 'c')
    
    # Convert suits to list
    allSuits = df_suits.values.tolist()
    return allSuits
    
# Scores
def formatScores(df_test):
    scores = df_test.loc[:, 10].values.tolist()
    return scores
    
#%% Unit test handValues

def test_evaluateHand(testData=testData):
    # Import Test Data
    df_test = importTestData(testData)
    
    # Format Test Data
    allValues, allSuits, scores = formatTestData(df_test)
    
    for i in range(len(allValues)):
        # Get values, suits, and test score
        values = allValues[i]
        suits = allSuits[i]
        testScore = scores[i]
        
        # Get hand score
        handScore = math.floor(evaluateHand(values, suits))
        assert handScore == testScore
        
