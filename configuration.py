# name: configuration
# description: Python file for playing Peg Solitaire with all possible configurations in Z_n
# author: Gustavo Sopena
# date started: Friday: June 28, 2019

import PegGame
import factory
import xlsxwriter
import math
import argparse
import sys

# setup the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--type', type=str, help="the type of graph to use: path, circle, windmill, doublestar", metavar='type', choices=['path', 'circle', 'windmill', 'doublestar'], required=True)
parser.add_argument('-s', '--size', type=int, help="the number of vertices for the graph", metavar='size', default=3)
parser.add_argument('-n', '--colorset', type=int, help="the color set: Z_n = (0, 1, ..., n-1) (default: 3)", metavar='n', default=3)
parser.add_argument('--leftSize', type=int, help="the number of vertices for the left side of the double star graph", metavar='L', default=0)
parser.add_argument('--rightSize', type=int, help="the number of vertices for the right side of the double star graph", metavar='R', default=0)
parser.add_argument('--bladeCount', type=int, help="the number of blades for the windmill graph", metavar='B', default=1)
parser.add_argument('--limit', type=int, help="the number of recursions allowed", metavar='m', default=1000)
args = parser.parse_args()

# set the desired type of graph
# set the desired size of graph
# set the desired color set, e.g., Z_3 = (0, 1, 2)
type = args.type
n = PegGame.n = args.colorset
if type == 'path' or 'circle':
    size = args.size
    G = factory.makeGraph(size, type)
if type == 'windmill':
    size = args.bladeCount * 2 + 1
    G = factory.makeWindmillGraph(args.bladeCount)
if type == 'doublestar':
    size = args.leftSize + args.rightSize + 2
    G = factory.makeDoubleStarGraph(args.leftSize, args.rightSize)

# the configuration, C, does not need to set manually
# they are going to found automatically

# set recursion limit
# create the file name for this game
# warning: if a file with the same name exists, it will override that file
sys.setrecursionlimit(args.limit)
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
# use the stopwatch to time playing games
# the outer 'for loop' sets the vertex position of the zero, starting at vertex 1
# the inner 'for loop' sets the configuration for the program to play
wonGames = 0
gameIndex = 1
with factory.stopwatch():
    for zeroPosition in range(1, size+1):
        # find the configurations based on the zero positions
        configurations = factory.findConfigurationsForGraphSizeAndColor(size, n, zeroPosition)

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
