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
parser.add_argument('--range', type=int, nargs=2, help="the numbered games to play", metavar=('a','b'))
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
# they are going to be found automatically

# set the total number of games
totalGames = int(math.pow(n-1, size-1)) * size

# every zero position defines a section with a fixed number of games
gamesPerSection = int(totalGames / size)

# if the range is provided, then check for valid selection
if args.range is not None:
    a = args.range[0]
    b = args.range[1]

    if a > b:
        parser.error("argument --range: invalid argument value order")
    elif a == b:
        parser.error("argument --range: argument values cannot be equal")
    elif (a < 1) or (b > totalGames):
        parser.error("argument --range: argument values exceed valid number of games")

    # determine the game start and end sections
    for s in range(1, size+1):
        # print("Checking Interval: "+str((s-1)*gamesPerSection+1)+", "+str(s*gamesPerSection))
        if (s-1)*gamesPerSection+1 <= a <= s*gamesPerSection:
            # print("a in section: "+str(s))
            startingZeroPosition = s
        if (s-1)*gamesPerSection+1 <= b <= s*gamesPerSection:
            # print("b in section: "+str(s))
            endingZeroPosition = s
            break
else:
    # if the range is not provided, then play all the games
    a = 1
    b = totalGames
    startingZeroPosition = 1
    endingZeroPosition = size

# set recursion limit
# create the file name for this game
# warning: if a file with the same name exists, it will override that file
sys.setrecursionlimit(args.limit)
fileName = 'peg-solitaire'+'-'+type+'-'+'s'+str(size)+'-'+'z'+str(n)+'-'+'r['+str(a)+'-'+str(b)+']'+'.xlsx'
print("Saving to file: "+fileName)

# open the workbook and add a worksheet (additionally, set text formatting)
# begin row at 0
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold':True})
boldright = workbook.add_format({'align':'right', 'bold':True})
row = 0

# set counter to determine number of games won
# set counter to determine number of games lost
# set counter for the current game
# use the stopwatch to time playing games
# the outer 'for loop' sets the vertex position of the zero
# the inner 'for loop' sets the configuration for the program to play
wonGames = 0
lostGames = 0
gameIndex = a
with factory.stopwatch():
    for zeroPosition in range(startingZeroPosition, endingZeroPosition+1):
        # if 'a' and 'b' exist in the same section, play the desired games
        # if 'a' and 'b' exist in different sections, play the desired starting game, the desired ending game, and all games in between
        if startingZeroPosition == endingZeroPosition:
            # 'a' should not be the right endpoint of the section
            # 'b' should not be the left endpoint of the section
            alpha = a % gamesPerSection
            alpha = alpha - 1 if alpha is not 0 else alpha
            beta = b % gamesPerSection
            beta = beta if beta is not 0 else gamesPerSection
        elif zeroPosition == startingZeroPosition:
            # 'a' can be the right endpoint of the section
            alpha = a % gamesPerSection
            alpha = alpha - 1 if alpha is not 0 else gamesPerSection - 1
            beta = gamesPerSection
        elif zeroPosition == endingZeroPosition:
            # 'b' can be the left endpoint of the section
            alpha = 0
            beta = b % gamesPerSection
            beta = beta if beta is not 0 else gamesPerSection
        else:
            alpha = 0
            beta = gamesPerSection

        # find the configurations based on the zero position
        configurations = factory.findConfigurationsForGraphSizeAndColor(size, n, zeroPosition)[alpha:beta]

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

            # increase won/lost counter
            if result == True:
                wonGames += 1
            else:
                lostGames += 1

            # increase current game counter
            gameIndex += 1
            row += 1

worksheet.write(row, 0, "Total")
worksheet.write(row, 1, totalGames)
print("Total: "+str(int(totalGames)))
row += 1

worksheet.write(row, 0, "Played")
worksheet.write(row, 1, b-a+1)
print("Played: "+str(b-a+1))
row += 1

worksheet.write(row, 0, "Won")
worksheet.write(row, 1, wonGames)
print("Won: "+str(wonGames))
row += 1

worksheet.write(row, 0, "Lost")
worksheet.write(row, 1, lostGames)
print("Lost: "+str(lostGames))

workbook.close()
