# name: game
# description: The peg solitaire implementation, using an iterative method
# author: Dr. Matthew Rathbun, Gustavo Sopena
# date started: Monday: July 20, 2020

# the number of colors available for playing
# in principle, the game can be easily changed to accommodate Z_n, by simply changing this parameter
n = 3

# the following function builds all the possible moves for a given "Graph" with "Configuration"
# it returns a list of lists, where each inner list consists of three vertices (in order), denoting a 'move'
def build_moves(Graph, Configuration):
    possible_moves = []

    for vertex in Graph: # cycle through each "vertex" in the "Graph"
        # check that a peg exists in this vertex
        if Configuration[vertex] != 0:
            for connected_vertex in Graph[vertex]: # cycle through each vertex connected to the first
                # check that a peg exists in the the connected vertex
                if Configuration[connected_vertex] != 0:
                    for next_connected_vertex in Graph[connected_vertex]: # cycle through each vertex connected to the second one
                        # check that a peg does NOT exist in the third vertex
                        if Configuration[next_connected_vertex] == 0:
                            # add a possible move to the list
                            possible_moves.append([vertex, connected_vertex, next_connected_vertex])
                        else:
                            pass
                else:
                    pass
        else:
            pass

    return possible_moves

# the following function executes a given "Move" on a given "Graph" with "Configuration"
# it returns a dictionary, denoting the resulting configuration of pegs after the "Move"
# an exception is raised if an invalid move is attempted
def execute_move(Graph, Configuration, Move):
    # Move[0] refers to the vertex of the jumping peg, Move[1] refers to the vertex being jumped, and Move[2] refers to the vertex being jumped into
    # check that the second vertex of the "Move" is actually connected to the first vertex of the "Move", and that the third is actually connected to the second (cross-referencing the "Configuration" with the Graph)
    # check that the first vertex actually has a peg in it
    # check that the second vertex actually has a peg in it
    # check that the third vertex does NOT have a peg in it
    if Move[1] in Graph[Move[0]] and Move[2] in Graph[Move[1]] and Configuration[Move[0]] != 0 and Configuration[Move[1]] != 0 and Configuration[Move[2]] == 0:
        # copy the given configuration
        # set the third vertex peg value to that of first vertex
        # remove the peg from the first vertex, effectively moving the peg
        # change the value of the peg at second vertex to the sum of the two peg values (mod n)
        # return a list with the original "Graph" and the resulting configuration of pegs
        new_configuration = Configuration.copy()
        new_configuration[Move[2]] = Configuration[Move[0]]
        new_configuration[Move[0]] = 0
        new_configuration[Move[1]] = (Configuration[Move[0]] + Configuration[Move[1]])%n
        return new_configuration
    else:
        raise Exception("An invalid move has been attempted.")

# the following function executes all "Moves" on a given "Graph" with "Configuration"
# it returns a list of dictionaries, denoting all resulting configurations obtained after executing all "Moves"
def execute_all_moves(Graph, Configuration, Moves):
    resulting_configurations = []

    for move in Moves:
        resulting_configurations.append(execute_move(Graph, Configuration, move))

    return resulting_configurations

# the following function checks whether the given "Configuration" is in a state that is considered a win
# it returns a boolean value denoting if the win condition was satisfied
# an exception is raised if all vertices contain a zero peg value, which should not occur through normal play
def satisfies_win_condition(Configuration):
    peg_count = 0
    for vertex in Configuration:
        if Configuration[vertex] > 0:
            peg_count += 1

    if peg_count > 1:
        return False
    elif peg_count == 1:
        return True
    else:
        raise Exception("All vertices contain a zero peg value.")

# the following workhorse function determines whether a "Graph" with "Configuration" has a winning 'sequence' of moves
# it returns a boolean value denoting if a 'sequence' of configurations was found, and every configuration 'seen' during the play-through
def is_winnable(Graph, Configuration):
    # a list of lists, where each inner list consists of a "Configuration" of the "Graph" and its depth in the outer list (main list)
    # a list of configurations 'seen' during the play-through
    # the iterator traversing forwards in the main list
    # the boolean value that determines whether a configuration satisfied the win condition
    # the current item from the main list
    # the depth of the current item
    # the index of the current item
    main_list = [[Configuration, 0]]
    seen = [Configuration]
    item = iter(main_list)
    did_satisfy_win_condition = False
    current_item = None
    current_depth = 0
    current_index = 0

    while True:
        try:
            current_item = next(item)
            current_depth = current_item[1]
        except StopIteration as stop_iteration_error:
            break

        if satisfies_win_condition(current_item[0]):
            did_satisfy_win_condition = True
            current_index = main_list.index(current_item)
            break

        all_moves = build_moves(Graph, current_item[0])
        if len(all_moves) == 0:
            continue

        filtered_configurations = []
        all_configurations = execute_all_moves(Graph, current_item[0], all_moves)

        for cn in all_configurations:
            if cn in seen:
                continue
            else:
                seen.append(cn)
                filtered_configurations.append(cn)

        if len(filtered_configurations) == 0:
            continue

        current_index = main_list.index(current_item)
        counter = 0
        for fd_cn in filtered_configurations:
            main_list.insert(current_index+counter+1, [fd_cn, current_depth+1])
            counter += 1

    # the 'sequence' list of configurations that results in a win
    # the iterator traversing backwards in the main list
    sequence = []
    if did_satisfy_win_condition:
        sequence.append(current_item[0])
        item = reversed(main_list[0:current_index])

        counter = 0
        while True:
            current_item = next(item)

            if current_item[1] == (current_depth-counter)-1:
                sequence.insert(0, current_item[0])
                counter += 1

            if current_item[1] == 0:
                break

        return True, sequence, seen
    else:
        return False, sequence, seen
