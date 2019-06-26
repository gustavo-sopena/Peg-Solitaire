### Graph will be represented by dictionary = { 1: [2, 3], 2: [1, 4, 5], ...} where:
###     vertices are labeled by integers (my convention has been to start at 1),
###     each vertex/integer is a key in the dictionary,
###     the value of each key is a list of every vertex linked to key by an edge
### Example 1: A three-vertex path graph would be {1: [2], 2: [1, 3], 3: [2]}
### Example 2: A three-vertex loop graph (a triangle) would be {1: [2, 3], 2: [1, 3], 3: [1, 2]}

### Position will be represented by a dictionary = {1: 0, 2: 3, ...} where:
###     each vertex/integer is a key in the dictionary,
###     the value of each key is the value in Z_3 = {0, 1, 2} of the peg at that vertex

### move will be a list of three integers = [v1, v2, v3] where:
###     v1 is the vertex of the peg to be moved
###     v2 is the vertex of the peg to be jumped over
###     v3 is the vertex to be jumped to

n = 3
### In principle, the game could be easily changed to accommodate Z_n, but
### the addition rules for how jumped pegs change values may need to be adjusted as well 
### as simply changing this parameter.

### This function lists all the possible moves available on a given "Graph" with a given 
### "Position" of pegs.
### The output is a list of lists - each item in the list is a "move", which is a list of three vertices (in order).
def moves(Graph, Position):
    possible_moves = [] #Initialize an empty list
    for vertex in Graph: #Cycle through each "vertex" in the "Graph"
        if Position[vertex] != 0: #Check that there is a peg at that vertex. If not, move on
            for connected_vertex in Graph[vertex]: #If so, then cycle through each vertex connected to the first.
                if Position[connected_vertex] != 0: #Check that the connected vertex has a peg. If not, move on.
                    for next_connected_vertex in Graph[connected_vertex]: #Cycle through each vertex connected to the second one. 
                        if Position[next_connected_vertex] == 0: #Check that the third vertex does NOT have a peg. If so, move on. 
                            possible_moves.append([vertex, connected_vertex, next_connected_vertex]) #Add a possible move to the list.
                        else:
                            pass
                else:
                    pass
        else:
            pass
    return possible_moves #Return the list

### This function applies a given "move" to a given "Graph" and "Position" of pegs.
### It returns a list of two items, the original "Graph" and a "New_position" of pegs after the move.      
def make_move(Graph, Position, move):
    #This is a long condition. move[0] refers to the vertex of the jumping peg, move[1] to the vertex being jumped, 
    # and move[2] to the ending position.
    #Check that the second vertex of the move is actually connected to the first vertex of the move,
    # and that the third is actually connected to the second (cross-referencing the Position with the Graph).
    #Check that the first vertex actually has a peg in it.
    #Check that the second vertex actually has a peg in it.
    #Check that the third vertex does NOT have a peg in it.
    if move[1] in Graph[move[0]] and move[2] in Graph[move[1]] and Position[move[0]] != 0 and Position[move[1]] != 0 and Position[move[2]] == 0:
        New_position = Position.copy() #Copy the starting position.
        New_position[move[2]] = Position[move[0]] #Set the third vertex peg value to that of first vertex.
        New_position[move[0]] = 0 #Remove the peg from the first vertex, effectively 'moving' it.
        New_position[move[1]] = (Position[move[1]] + Position[move[0]])%n #Change the value of the peg at second vertex to the sum of the two 
                                                                          #peg values (mod n).
        return [Graph, New_position] #Return a list with the original "Graph" and the resulting "New_position" of pegs.
    else:
        raise Exception("An illegal move has been attempted.") #Raises an error and interrupts program just in case 
                                                               #an illegal move is attempted. 

### This function runs through the list of every possible move for a given position,
### plays each move, and returns a list of lists - each item is a two-item list consisting of 
### the "Graph" and the "resulting_position" of the corresponding move.        
def play_all_moves(Graph, Position):
    resulting_positions = [] #Initializes an empty list
    all_moves = moves(Graph, Position) #Applies the "moves" function above to generate every possible move for the current "Position".
    for move in all_moves: #Runs through each "move" in the list
        resulting_positions.append(make_move(Graph, Position, move)[1]) #Makes "move", then extracts the resulting position from 
                                                                        #the function output, and appends it to the list of positions.
    return [[Graph, resulting_position] for resulting_position in resulting_positions] #Returns a list of two-item lists, 
                                                                                       #each the "Graph" and one of the resulting positions.

### This function checks whether the current "Position" is actually already in an end state that counts as a win.     
def won(Graph, Position):
    remaining = 0 #Initializes the count of "remaining" pegs to zero.
    for peg in Position: #Runs through each peg value for each vertex
        if Position[peg] > 0: #If there is a non-zero peg value at that vertex, add one to the "remaining" counter 
                              #(regardless of what the value of the peg is at the vertex). 
            remaining += 1
    if remaining > 1: #If there was more than one vertex that had a non-zero peg value, then return False - the game is not currently won.
            return False
    elif remaining == 1:
        return True #If there is just one vertex with a non-zero peg value, then return True - the game is currently won.
    else:
        raise Exception("It should not be possible to have a completely empty board.") #Raises an error and interrupts program 
                                                                                       #just in case somehow the board has no pegs at all, 
                                                                                       #which should not occur through normal play. 

### This function runs through all the possible moves and the resulting positions, and decides whether 
### the current position has any single move that results in a win.        
def winning_move(Graph, Position):
    if won(Graph, Position): #If the current position is already at the winning condition, return True and the current (winning) "Position"
        return True, Graph, Position
    else:
        if len(moves(Graph, Position)) > 0: #Otherwise, check whether there are possible moves to perform.
            for result in play_all_moves(Graph, Position): #For ech move, the result is the Graph and a resulting position
                if won(result[0], result[1]): #Check whether that resulting Graph and Position satisfy the winning condition.
                    return True, Graph, result[1] #If so, return True, the Graph, and the resulting winning position.
            return False, None, None #If none of the results satisfied the winning condition, return False (and two Nones, for the sake of 
                                     #having the same sized output as when returning True.
        else:
            return False, None, None #If there were no moves to perform, and we haven't already won, return False (and two Nones).

### This is the workhorse function. It determines whether a "Graph" and "Position" have a winning sequence of moves.
### This function will call itself, recursively. 
### If the "Position" is winnable, the function will return True, the "Graph", a list of a winning sequence of board positions resulting in the win,
###  and a list of every board position the function saw during its search. The useful data should be the True (index 0) and 
###  the winning "sequence" (index 2)
### If the "Position" is not winnable, the function will return False, the "Graph", and empty list, and a list of every board position 
###  the function saw during its search. The useful data should be the False (index 0), and possibly the "seen" list, though it will be 
###  pretty difficult to parse through.
def winnable(Graph, Position, sequence=[], seen=[]): #The default values of "sequence" and "seen" are empty lists, so that the function
                                                     #can be called without this data, but then allows recursive calls of the function to
                                                     #carry the accumulated data along.
    if len(sequence)==0: 
        sequence.append(Position) #Add the starting "Position" to the "sequence" list at the initial call of the function.
    if len(seen)==0:
        seen.append(Position) #Add the starting "Position" to the "seen" list at the initial call of the function.
    bool, gr, pos = winning_move(Graph, Position) #Ask whether the "Position" has a single winning move. Returns a Boolean, the "Graph", 
                                                  #and a "Position" (or a Boolean, None, and None)
    if bool: #If the Boolean value is True, this was because there was a winning move.
        sequence.append(pos) #Add the resulting position that satisfies the winning condition to the "sequence".
        seen.append(pos) #And add it to the "seen" list.
        return True, Graph, sequence, seen #Return True, the "Graph", "sequence", and "seen".
    else:
        level = [] #Otherwise, initialize an empty list.
        for curr_move in moves(Graph, Position): #Run through all the possible moves
            [new_graph, new_pos] = make_move(Graph, Position, curr_move) #Make each move
            if new_pos in seen: #If the move results in a graph that has already been explored, then don't do anything.
                continue #Continue moves on to the next item in the for loop.
            seq = sequence[:] #Make a copy of the "sequence" list to correspond to the current move in the loop.
            seq.append(new_pos) #Add the resulting position to this "seq"uence.
            seen.append(new_pos) #Add the resulting position to the global tally "seen".
            level.append(winnable(new_graph, new_pos, seq, seen)) #Determine whether the resulting position is "winnable" with a recursive
                                                                  #call to this function, passing the information about what has been "seen"
                                                                  #and the "seq"uence relevant to the current move that has resulted in this 
                                                                  #position (that the recursive call is being applied to).
        for result in level: #Once "level" has been populated with the results of whether each possible move for "Position"
                             #resulted in a "winnable" position, run through to see if any of those answers were yes.
            if result[0]: #The first item in result is a Boolean. If it is True, this corresponds to a "winnable" position.
                return True, Graph, result[2], result[3] #Return True, the "Graph", and the third and fourth items in "result", namely,
                                                         #the lists "seq" and "seen".
        else:
            return False, Graph, [], seen #Otherwise, return False, the "Graph", an empty list, and the list "seen"
        ###Each recursive call to the function hands its result back up to the previous call to populate the list "level".
        ###If "level" consists of all results with Falses, the current call of the function will either return the negative result,
        ### or will hand that result up to a previous call of the function to populate an earlier "level".
        ###If "level" has a result with True, then the current call either returns the first instance of that positive result,
        ### or will hand that positive result up to a previous call of the function to populate an earlier "level".
