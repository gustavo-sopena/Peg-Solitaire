# name: configuration
# description: Python file for playing Peg Solitaire with all possible configurations in Z_n
# author: Gustavo Sopena
# date started: Friday: June 28, 2019

import PegGame
import factory
import xlsxwriter
import math

# set the color set to use, match this in factory.py and PegGame.py as well
# e.g., Z_3 = (0, 1, 2)
# set the number of vertices for the graph (int)
# set the type of graph (string)
# for now, options are: circle, path
n = 3
size = 3
type = 'circle'
G = factory.makeGraph(size, type)

# the configuration, C, does not need to set manually
# they are going to found automatically

# create the file name for this game
# warning: if a file with the same name exists, it will override that file
fileName = 'peg-solitaire-configuration-sheet'+'-'+type+'-'+str(size)+'-'+'z'+str(n)+'.xlsx'
print("Saving to file: "+fileName)

# open the workbook and add a worksheet (additionally, set text formatting)
# begin row at 0
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold':True})
boldright = workbook.add_format({'align':'right', 'bold':True})
row = 0

# set the total number of games
totalGames = math.pow(n-1, size-1) * size
# halfGames = totalGames / 2

# set counter to determine number of games won
# set counter for the current game
# the outer 'for loop' sets the vertex position of the zero, starting at vertex 1
# the inner 'for loop' sets the configuration for the program to play
wonGames = 0
gameIndex = 1
for zeroPosition in range(1, size+1):
    # find the configurations based on the zero positions
    configurations = factory.findConfigurationsForGraphSize(size, zeroPosition)

    for config in configurations:
        # write a header-like row in the excel file for the current game
        worksheet.write(row, 0, "Game", bold)
        worksheet.write(row, 1, gameIndex, bold)
        row += 1

        # show current game, update the row index
        factory.writeConfigurationToSheet(config, row, worksheet)
        row += 1

        # play the game
        result, graph, sequence, seen = PegGame.winnable(G, config, [], [])

        # show if the game won
        worksheet.write(row, 0, "Win", bold)
        worksheet.write(row, 1, str(result), boldright)
        row += 1

        # show series of moves that won the game, if any
        for c in sequence:
            factory.writeConfigurationToSheet(c, row, worksheet)
            row += 1

        # show the games that the program found while playing
        # worksheet.write(row, 0, "Seen List")
        # row += 1
        # for c in seen:
        #     factory.writeConfigurationToSheet(c, row, worksheet)
        #     row += 1

        # if the game is winnable, then increase counter
        if result == True:
            wonGames += 1

        # increase current game counter
        gameIndex += 1
        row += 1

        # check if we played half of the games
        # if gameIndex == halfGames + 1:
        #     break

worksheet.write(row, 0, "Total")
worksheet.write(row, 1, totalGames)
print("Total: "+str(int(totalGames)))
row += 1

worksheet.write(row, 0, "Played")
worksheet.write(row, 1, gameIndex-1)
print("Played: "+str(gameIndex-1))
row += 1

worksheet.write(row, 0, "Won")
worksheet.write(row, 1, wonGames)
print("Won: "+str(wonGames))
row += 1

worksheet.write(row, 0, "Lost")
worksheet.write(row, 1, gameIndex-wonGames-1)
print("Lost: "+str(gameIndex-wonGames-1))

workbook.close()
