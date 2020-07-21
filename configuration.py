# name: configuration
# description: Python file for playing Peg Solitaire with all possible configurations in Z_n
# author: Gustavo Sopena
# date started: Friday: June 28, 2019

import game
import factory
import xlsxwriter
import argparse
import sys

# setup the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-e', action="store_true", help="switch to a descriptive file name: i.e. 'ps.xlsx' to 'peg-solitaire.xlsx'")
parser.add_argument('-t', '--type', type=str, help="the type of graph to use: path, circle, windmill, doublestar", metavar='type', choices=['path', 'circle', 'windmill', 'doublestar'], required=True)
parser.add_argument('-s', '--size', type=int, help="the number of vertices for the graph", metavar='size', default=3)
parser.add_argument('-n', '--colorset', type=int, help="the color set: Z_n = (0, 1, ..., n-1) (default: 3)", metavar='n', default=3)
parser.add_argument('--leftSize', type=int, help="the number of vertices for the left side of the double star graph", metavar='L', default=0)
parser.add_argument('--rightSize', type=int, help="the number of vertices for the right side of the double star graph", metavar='R', default=0)
parser.add_argument('--bladeCount', type=int, help="the number of blades for the windmill graph", metavar='B', default=1)
parser.add_argument('--limit', type=int, help="the number of recursions allowed", metavar='m', default=1000)
parser.add_argument('--range', type=int, nargs=2, help="the numbered games to play: [a, b]", metavar=('a','b'))
parser.add_argument('--dry-run', action="store_true", help="simulate playing the game")
args = parser.parse_args()

# set the desired type of graph
# set the desired size of graph
# set the desired color set, e.g., Z_3 = (0, 1, 2)
typeDescriptive = args.type
n = game.n = args.colorset
if typeDescriptive == 'path':
    size = args.size
    typeCompact = 'p'
    sizeDescription = size
    G = factory.makeGraph(size, typeDescriptive)
if typeDescriptive == 'circle':
    size = args.size
    typeCompact = 'c'
    sizeDescription = size
    G = factory.makeGraph(size, typeDescriptive)
if typeDescriptive == 'windmill':
    size = args.bladeCount * 2 + 1
    typeCompact = 'w'
    sizeDescription = args.bladeCount
    G = factory.makeWindmillGraph(args.bladeCount)
if typeDescriptive == 'doublestar':
    size = args.leftSize + args.rightSize + 2
    typeCompact = 'ds'
    sizeDescription = str(args.leftSize)+'-'+str(args.rightSize)
    G = factory.makeDoubleStarGraph(args.leftSize, args.rightSize)

# set the total number of games
totalGames = ((n-1) ** (size-1)) * size

# every zero position defines a section with a fixed number of games
gamesPerSection = int(totalGames / size)

# if the range is provided, then check for valid selection
if args.range is not None:
    a = args.range[0]
    b = args.range[1]

    if a > b:
        print("configuration.py: error: argument --range: invalid argument value order")
        sys.exit()
    elif a == b:
        print("configuration.py: error: argument --range: argument values cannot be equal")
        sys.exit()
    elif (a < 1) or (b > totalGames):
        print("configuration.py: error: argument --range: invalid argument values: choose from [{}, {}] (inclusive)".format(1, totalGames))
        sys.exit()

    # determine the game start and end sections
    for s in range(1, size+1):
        # print("Checking Interval: "+str((s-1)*gamesPerSection+1)+", "+str(s*gamesPerSection))
        if (s-1)*gamesPerSection+1 <= a <= s*gamesPerSection:
            # print("a in section: "+str(s))
            currentSection = s
            startingZeroPosition = s
        if (s-1)*gamesPerSection+1 <= b <= s*gamesPerSection:
            # print("b in section: "+str(s))
            endingZeroPosition = s
            break
else:
    # if the range is not provided, then play all the games
    a = 1
    b = totalGames
    currentSection = 1
    startingZeroPosition = 1
    endingZeroPosition = size

# set recursion limit
# create the file name for this game
# warning: if a file with the same name exists, it will override that file
sys.setrecursionlimit(args.limit)
fileName = "{}-ti({})-zi({})-ri[{}-{}].xlsx"
if args.e:
    fileName = fileName.format('peg-solitaire', sizeDescription, n, a, b)
    fileName = fileName.replace('ti', typeDescriptive).replace('zi', "colorset").replace('ri', "range")
else:
    fileName = fileName.format('ps', sizeDescription, n, a, b)
    fileName = fileName.replace('ti', typeCompact).replace('zi', "z").replace('ri', "r")
print("Generating File: {}".format(fileName))
print("")

# simulate playing games
if args.dry_run:
    print("Processing:")
    for zeroPosition in range(startingZeroPosition, endingZeroPosition+1): # use zeroPosition as current section ?
        print("Configuration Section ({}): Playing... Done.".format(currentSection))
        currentSection += 1

    print("")
    print("Calculating Time... Done.")
    print("Saving xlsx File... Done.")
    print("")
    print("Statistics:")
    print("Time: -- hours = -- minutes = -- seconds")
    print("Total: {}".format(totalGames))
    print("Played: {}".format(b-a+1))
    print("Won: --")
    print("Lost: --")
    print("Size: {}".format(size))
    print("Span: {}".format(gamesPerSection))
    print("Sections: {}".format(int(totalGames / gamesPerSection)))
    sys.exit()

# open the workbook and add a worksheet (additionally, set text formatting)
# begin row at 0
workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
right = {'align':'right'}
bold = {'bold':True}
border = {'border':True}
borderColor = {'border_color':"gray"}
cellBackgroundColor = {'bg_color':'#D0D0D0'}
row = 3

# set counter to determine number of games won
# set counter to determine number of games lost
# set counter for the current game
# use the stopwatch to time playing games
# the outer 'for loop' sets the vertex position of the zero
# the inner 'for loop' sets the configuration for the program to play
wonGames = 0
lostGames = 0
gameIndex = a
recursionError = False
with factory.stopwatch(worksheet, workbook.add_format(right)):
    print("Processing:")
    for zeroPosition in range(startingZeroPosition, endingZeroPosition+1):
        # if 'a' and 'b' exist in the same section, play the desired games
        # if 'a' and 'b' exist in different sections, play the desired starting game, the desired ending game, and all games in between
        if startingZeroPosition == endingZeroPosition:
            # 'a' should not be the right endpoint of the section
            # 'b' should not be the left endpoint of the section
            alpha = a % gamesPerSection
            alpha = alpha if alpha != 0 else alpha
            beta = b % gamesPerSection
            beta = beta if beta != 0 else gamesPerSection
        elif zeroPosition == startingZeroPosition:
            # 'a' can be the right endpoint of the section
            alpha = a % gamesPerSection
            alpha = alpha if alpha != 0 else gamesPerSection
            beta = gamesPerSection
        elif zeroPosition == endingZeroPosition:
            # 'b' can be the left endpoint of the section
            alpha = 1
            beta = b % gamesPerSection
            beta = beta if beta != 0 else gamesPerSection
        else:
            alpha = 1
            beta = gamesPerSection

        # find the configurations based on the zero position
        print("Configuration Section ({}): ".format(currentSection), end="", flush=True)
        configurations = factory.buildConfigurations(size, n, zeroPosition, alpha, beta)

        print("Playing... ", end="", flush=True)
        for config in configurations:
            # write a header-like row in the excel file for the current game
            worksheet.set_row(row, cell_format=factory.makeSheetCellFormat(workbook, bold, cellBackgroundColor, border, borderColor))
            worksheet.write(row, 0, "Game")
            worksheet.write(row, 1, gameIndex)
            row += 1

            # show current game, update the row index
            factory.writeConfigurationToSheet(config, row, worksheet)
            row += 1

            # on this row in the excel file: show whether the game was winnable or failed to determined
            worksheet.write(row, 0, "Win", workbook.add_format(bold))

            # play the game
            try:
                result, graph, sequence, seen = game.winnable(G, config, [], [])
            except RecursionError:
                # break from playing other games if a recursion error occurs (for now)
                recursionError = True
                worksheet.write(row, 4, "Failed To Determine: Recursion Error", factory.makeSheetCellFormat(workbook, bold, right))
                row += 2
                break

            # show if the game won
            worksheet.write(row, 1, str(result), factory.makeSheetCellFormat(workbook, bold, right))
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

        currentSection += 1
        print("Done.") if recursionError != True else print("Failed To Determine: Recursion Error.")

    print("")
    print("Calculating Time... Done.")
    print("Saving xlsx File... Done.")
    print("")
    print("Statistics:")

# row, column
worksheet.set_row(0, cell_format=factory.makeSheetCellFormat(workbook, bold, cellBackgroundColor, border, borderColor))

worksheet.write(0, 0, "Total")
worksheet.write(1, 0, totalGames)
print("Total: {}".format(totalGames))

worksheet.write(0, 1, "Played")
worksheet.write(1, 1, b-a+1)
print("Played: {}".format(b-a+1))

worksheet.write(0, 2, "Won")
worksheet.write(1, 2, wonGames)
print("Won: {}".format(wonGames))

worksheet.write(0, 3, "Lost")
worksheet.write(1, 3, lostGames)
print("Lost: {}".format(lostGames))

worksheet.write(0, 4, "Size")
worksheet.write(1, 4, size)
print("Size: {}".format(size))

worksheet.write(0, 5, "Span")
worksheet.write(1, 5, gamesPerSection)
print("Span: {}".format(gamesPerSection))

worksheet.write(0, 6, "Sections")
worksheet.write(1, 6, int(totalGames / gamesPerSection))
print("Sections: {}".format(int(totalGames / gamesPerSection)))

workbook.close()
