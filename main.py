# name: main (driver)
# description: Python Driver file for playing Peg Solitaire
# author: Gustavo Sopena
# date started: Friday: June 28, 2019

import PegGame
import gamesetup

size = 3
G = gamesetup.makeGraph(size, 'circle')

wonGames = 0
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
