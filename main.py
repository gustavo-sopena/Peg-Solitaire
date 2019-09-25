# name: main
# description: Python Script to play games
# author: Gustavo Sopena
# date started: Thursday: July 5, 2019

import PegGame
import factory
import xlsxwriter
# import math

# set the color set to use, match this in PegGame.py as well
# e.g., Z_3 = (0, 1, 2)
# set the number of vertices for the graph (int)
# set the type of graph (string)
# for now, options are: circle, path
n = 3
size = 5
type = 'path'
G = factory.makeGraph(size, type)

# set the configuration for the graph
C = {1:0, 2:1, 3:1, 4:1, 5:1}

# create the file name for this game
# warning: if a file with the same name exists, it will override that file
fileName = 'peg-solitaire-example-sheet'+'-'+type+'-'+str(size)+'-'+'z'+str(n)+'.xlsx'
print("Saving to file: "+fileName)

# open the workbook and add a worksheet
# begin row at 0
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold':True})
boldright = workbook.add_format({'align':'right', 'bold':True})
row = 0

# there is only one game being played
# so, no game index for this file

# write a header-like row in the excel file for the current game
worksheet.write(row, 0, "Game", bold)
worksheet.write(row, 1, 0, bold)
row += 1

# show the current game
factory.writeConfigurationToSheet(C, row, worksheet)
row += 1

# play the game
result, graph, sequence, seen = PegGame.winnable(G, C)

# show if the game won
print("Win: "+str(result))
worksheet.write(row, 0, "Win", bold)
worksheet.write(row, 1, str(result), boldright)
row += 1

# optional: show the starting state
# factory.prettyPrintConfiguration(C)

# show series of moves that won the game, if any
for c in sequence:
    factory.prettyPrintConfiguration(c)
    factory.writeConfigurationToSheet(c, row, worksheet)
    row += 1

# show the games that the program saw while playing
# print("Seen List")
# for c in seen:
#     factory.prettyPrintConfiguration(c)

workbook.close()
