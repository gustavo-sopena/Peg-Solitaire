# name: main
# description: Python Script to play games
# author: Gustavo Sopena
# date started: Thursday: July 5, 2019

import PegGame
import setup
import xlsxwriter
import shutil
import os

# specify the number of vertices for the graph (int)
# specify the type of graph (string)
# for now, options are: circle, path
size = 8
type = 'circle'
G = setup.makeGraph(size, type)

# specify the configuration for the graph
C = {1:0, 2:2, 3:1, 4:2, 5:1, 6:2, 7:1, 8:2}

# create the file name for this game
# open the workbook and add a worksheet
# begin row at 0
fileName = 'peg-solitaire-example'+'-'+type+'-'+str(size)+'-'+'z3'+'.xlsx'
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
row = 0

# play the game
result, graph, sequence, seen = PegGame.winnable(G, C)

# show if the game won
# optional: show the starting state
print("Win: "+str(result))
# setup.prettyPrintConfiguration(C)

# check if the game is winnable
# if so, show the steps that lead to the win
for c in sequence:
    setup.prettyPrintConfiguration(c)
    setup.writeConfigurationToSheet(c, row, worksheet)
    row += 1

# show the games that the program saw while playing
# print("Seen List")
# for c in seen:
#     setup.prettyPrintConfiguration(c)

# close the workbook
# move the excel sheet into the folder "Sheets"
workbook.close()

try:
    shutil.move(fileName, 'Sheets/')
except shutil.Error as serr:
    os.remove(fileName)
