# name: main (driver)
# description: Python Driver file for playing Peg Solitaire
# author: Gustavo Sopena
# date started: Friday: June 28, 2019

import PegGame
import gamesetup
import xlsxwriter

size = 3
type = 'circle'
G = gamesetup.makeGraph(size, type)
fileName = 'peg-solitaire'+'-'+type+'-'+str(size)+'-'+'z3'+'.xlsx'
print("Saving to file: "+fileName)

workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold':True})
boldright = workbook.add_format({'align':'right', 'bold':True})

row = 0
wonGames = 0
gameIndex = 1
for zeroPosition in range(1, size+1):
    configurations = gamesetup.findConfigurationsForGraphSize(size, zeroPosition)

    for config in configurations:
        worksheet.write(row, 0, "Game", bold)
        worksheet.write(row, 1, gameIndex, bold)
        row += 1

        # show current game, update the row index
        gamesetup.writeConfigurationToSheet(config, row, worksheet)
        row += 1

        # play the game
        result, graph, sequence, seen = PegGame.winnable(G, config, [], [])
        worksheet.write(row, 0, "Win", bold)
        worksheet.write(row, 1, str(result), boldright)
        row += 1

        # show series of moves that won the game, if any
        for c in sequence:
            gamesetup.writeConfigurationToSheet(c, row, worksheet)
            row += 1

        # show the games that the program found while playing
        # worksheet.write(row, 0, "Seen List")
        # row += 1
        # for c in seen:
        #     gamesetup.writeConfigurationToSheet(c, row, worksheet)
        #     row += 1

        if result == True:
            wonGames += 1

        gameIndex += 1
        row += 1

worksheet.write(row, 0, "Total")
worksheet.write(row, 1, gameIndex-1)
print("Total: "+str(gameIndex-1))
row += 1

worksheet.write(row, 0, "Won")
worksheet.write(row, 1, wonGames)
print("Won: "+str(wonGames))
row += 1

worksheet.write(row, 0, "Lost")
worksheet.write(row, 1, gameIndex-wonGames-1)
print("Lost: "+str(gameIndex-wonGames-1))

workbook.close()
