# import PegGame

### Graph will be represented by dictionary = { 1: [2, 3], 2: [1, 4, 5], ...} where:
###     vertices are labeled by integers (my convention has been to start at 1),
###     each vertex/integer is a key in the dictionary,
###     the value of each key is a list of every vertex linked to key by an edge
### Example 1: A three-vertex path graph would be {1: [2], 2: [1, 3], 3: [2]}
### Example 2: A three-vertex loop graph (a triangle) would be {1: [2, 3], 2: [1, 3], 3: [1, 2]}

### Position will be represented by a dictionary = {1: 0, 2: 3, ...} where:
###     each vertex/integer is a key in the dictionary,
###     the value of each key is the value in Z_3 = {0, 1, 2} of the peg at that vertex

## Your graph goes here:
# G = {1: [9, 2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4, 6], 6: [5, 7], 7: [6, 8], 8: [7, 9], 9: [8,1]}
#G = {1: [2], 2: [1, 3], 3: [2]}

## Your starting position goes here:
# P = {1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6:1, 7:1, 8:2, 9:2}
#P = {1: 0, 2: 1, 3: 2}

## This applies the "winnable" function to the graph G and starting position P.
## The output has four items.
# result, graph, sequence, seen = PegGame.winnable(G, P)
## This prints two of the items, a Boolean "result", and "sequence" is either a sequence of 
## positions that results in a winning condition, or is an empty list if the "result" is False.
# print result, sequence

## If the result for a particular G and P is False, there may be interest in viewing the "seen"
## list as well, to look through all of the possible positions that result from all of the possible
## move combinations.

##########
# Example games
# All games played with n=3
##########

#P_3
#G = {1: [2], 2: [1,3], 3: [2]}
#P = {1: 2, 2: 2, 3: 0}
#Should be winnable
#Check

##########

#P_5
#G = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4]}

#P = {1: 1, 2: 2, 3: 0, 4: 2, 5: 0}
#Should be winnable
#Check

#P = {1: 0, 2: 0, 3: 1, 4: 2, 5: 0}
#Should be winnable
#Check

#P = {1: 1, 2: 1, 3: 0, 4: 0, 5: 0}
#Should be winnable
#Check

#P = {1: 1, 2: 1, 3: 0, 4: 1, 5: 0}
#Should be winnable
#Check

#P = {1: 1, 2: 1, 3: 0, 4: 0, 5: 1}
#Should be winnable
#Check

###########

#P_6
#G = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4, 6], 6: [5]}

#Ex 1
#P = {1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
#Known winnable
#Check

#Ex 2
#P = {1: 0, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2}
#Known winnable
#Check

#Ex 3
#P = {1: 0, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1}
#Known unwinnable
#Check

#Ex 4
#P = {1: 0, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2}
#E-mail unclear about winnability, but it looks like no?
#Program says no

##########

#C_5
#G = {1: [5, 2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4, 1]}

#Game 01
#P = {1: 0, 2: 1, 3: 1, 4: 1, 5: 1}
# Known winnable
#Check

#Game 03
#P = {1: 0, 2: 1, 3: 1, 4: 2, 5: 1}
# Known winnable
#Check

#Game 04
#P = {1: 0, 2: 1, 3: 1, 4: 2, 5: 2}
# Known winnable
#Check

#Game 05
#P = {1: 0, 2: 1, 3: 2, 4: 1, 5: 1}
# Known winnable
#Check

#Game 06
#P = {1: 0, 2: 1, 3: 2, 4: 1, 5: 2}
# Known winnable
#Check

#Game 08
#P = {1: 0, 2: 1, 3: 2, 4: 2, 5: 2}
# Known winnable
#Check

#Undecided case
#P = {1: 0, 2: 1, 3: 2, 4: 2, 5: 1}
#Unknown winnability
#Program says no!

##########

#W(2)
#G = {1: [2,3], 2: [1, 3, 4, 5], 3: [1, 2], 4: [2, 5], 5: [2, 4]}

#P = {1: 1, 2: 0, 3: 1, 4: 2, 5: 2}
#Known winnable
#Check

#P = {1: 0, 2: 1, 3: 1, 4: 1, 5: 1}
#Known winnable
#Check

##########

#W(1, 1)
#G = {1: [2, 3], 2: [1, 3], 3: [1, 2, 4], 4: [3]}

#P = {1: 1, 2: 1, 3: 0, 4: 1}
#Known winnable
#Check

##########

#Double-star (2,2)
#G = {1: [3], 2: [3], 3: [1, 2, 4], 4: [3, 5, 6], 5: [4], 6: [4]}

#P = {1: 0, 2: 1, 3: 1, 4: 2, 5: 1, 6: 2}
#Known winnable
#Check

##########

#Double-star (3,2)
#G = {1: [4], 2: [4], 3: [4], 4: [1, 2, 3, 5], 5: [4, 6, 7], 6: [5], 7: [5]}

#P = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0, 7: 1}
#Diagrammed game unclear - it looks like the ending is not a win, but this ending is not forced
#Program says winnable
# Here is the sequence of positions:
# [{1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0, 7: 1}, {1: 1, 2: 1, 3: 1, 4: 0, 5: 2, 6: 1, 7: 1}, {1: 1, 2: 1, 3: 1, 4: 1, 5: 0, 6: 0, 7: 1}, 
# {1: 0, 2: 1, 3: 1, 4: 2, 5: 1, 6: 0, 7: 1}, {1: 1, 2: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1}, {1: 1, 2: 0, 3: 1, 4: 1, 5: 2, 6: 0, 7: 0}, 
# {1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 0, 7: 0}, {1: 2, 2: 1, 3: 1, 4: 1, 5: 0, 6: 0, 7: 0}, {1: 2, 2: 0, 3: 1, 4: 2, 5: 1, 6: 0, 7: 0}, 
# {1: 0, 2: 2, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0}, {1: 1, 2: 2, 3: 0, 4: 2, 5: 1, 6: 0, 7: 0}, {1: 1, 2: 0, 3: 2, 4: 1, 5: 1, 6: 0, 7: 0}, 
# {1: 0, 2: 1, 3: 2, 4: 2, 5: 1, 6: 0, 7: 0}, {1: 2, 2: 1, 3: 0, 4: 1, 5: 1, 6: 0, 7: 0}, {1: 2, 2: 1, 3: 0, 4: 0, 5: 2, 6: 1, 7: 0}, 
# {1: 2, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0}, {1: 2, 2: 0, 3: 1, 4: 2, 5: 0, 6: 0, 7: 0}, {1: 0, 2: 2, 3: 1, 4: 1, 5: 0, 6: 0, 7: 0}, 
# {1: 1, 2: 2, 3: 0, 4: 2, 5: 0, 6: 0, 7: 0}, {1: 1, 2: 0, 3: 2, 4: 1, 5: 0, 6: 0, 7: 0}, {1: 0, 2: 1, 3: 2, 4: 2, 5: 0, 6: 0, 7: 0}, 
# {1: 0, 2: 1, 3: 0, 4: 1, 5: 2, 6: 0, 7: 0}, {1: 1, 2: 0, 3: 0, 4: 2, 5: 2, 6: 0, 7: 0}, {1: 1, 2: 0, 3: 0, 4: 0, 5: 1, 6: 2, 7: 0}, 
# {1: 1, 2: 0, 3: 0, 4: 2, 5: 0, 6: 0, 7: 0}, {1: 0, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}]
##########
