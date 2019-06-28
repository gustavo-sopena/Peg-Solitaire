# name: main (driver)
# description: Python Driver file for playing Peg Solitaire
# author: Gustavo Sopena
# date started: Friday: June 28, 2019

import PegGame
import gamesetup

# Graph of C_5
G = {1:[5,2], 2:[1,3], 3:[2,4], 4:[3,5], 5:[4,1]}

wonGames = 0
size = 5
gameIndex = 1
for zeroPosition in range(1, size+1):
    configurations = gamesetup.findConfigurationsForGraphSize(size, zeroPosition)

    for config in configurations:
        print("Game: "+str(gameIndex))
        gamesetup.prettyPrintConfiguration(config)
        print("")

        result, graph, sequence, seen = PegGame.winnable(G, config, [], [])
        print("Did Win: "+str(result))
        for c in sequence:
            gamesetup.prettyPrintConfiguration(c)

        print("")
        print("Seen List")
        for c in seen:
            gamesetup.prettyPrintConfiguration(c)
        print("")

        if result == True:
            wonGames += 1

        gameIndex += 1

print("Total Games: "+str(gameIndex-1))
print("Won Games: "+str(wonGames))
print("Lost Games: "+str(gameIndex-wonGames-1))
