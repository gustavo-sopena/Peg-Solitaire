# name: main
# description: Python Script that acts as a helper file for Peg Solitaire Research
# author: Gustavo Sopena
# date started: Friday: June 21, 2019

import math

# the following function prints the given configuration without brackets
def prettyPrintConfiguration(configuration):
    for vertex in configuration:
        pegColor = configuration[vertex]
        print(str(pegColor)+" ", end="")
    print("")

# the following function writes the given configuration to an xlsx file
def writeConfigurationToSheet(configuration, row, worksheet):
    for vertex in configuration:
        pegColor = configuration[vertex]
        worksheet.write(row, vertex-1, pegColor)

# the following function finds all of the configurations for the given graph size
# the output is a list of dictionaries
# for now we assume a path graph
def findConfigurationsForGraphSize(size, zeroPosition=1):
    tmpConfig = {}
    configList = []
    tmpList = []
    rowList = []
    listOneTwo = {1:2, 2:1}

    # obtain the length of the graph
    # graphSize = len(Graph) # no longer depends on the graph

    # set row to 1
    # set vertex to the last vertex index in the graph
    # set maximum number of rows for the configuration
    row = 1
    vertex = size
    maxRows = math.pow(2, size-1)
    printRows = maxRows

    # print(size)
    # print(maxRows)

    if size < 1:
        return {1:0}
    elif size == 2:
        return [{1:0, 2:1}, {1:0, 2:2}]
    else: # size == 3+
        # initialize the temporary configuration to zero
        for vertex in range(1, size+1):
            tmpConfig[vertex] = 0
        
        repeatFactor = 1
        which = 1
        while vertex > 0: # loop over the number of vertices
            while row < printRows+1: # loop over each row
                if which % 2 == 1:
                    which = 2
                elif which % 2 == 0:
                    which = 1

                # check how many times we have to print the current number
                index = 0
                while index < repeatFactor:
                    # print(listOneTwo[which])
                    tmpList.append(listOneTwo[which])
                    index += 1
                
                # update the row index
                row += 1
            
            # reduce the vertex by 1
            # reset the row to 1
            # double the repeat factor
            # half the number of max rows
            # save the temporary list into the master row list
            # reset the temporary list
            vertex -= 1
            row = 1
            repeatFactor *= 2
            printRows /= 2
            rowList.append(tmpList)
            tmpList = []
            # print("rf: "+str(repeatFactor))
        
        # print(maxRows)
        # print(rowList)
        row = 1
        vertex = size
        offset = 0
        while row < maxRows+1: # loop over each row
            while vertex > 1: # loop over the number of vertices
                if vertex == zeroPosition: # check if there should be a zero in this vertex
                    offset = 1
                
                tmpConfig[vertex-offset] = rowList[size-vertex][row-1]
                vertex -= 1
            
            # save the newly built configuration into the master configuration list
            # reset vertex to the number of vertices
            # update the row index
            # print(tmpConfig)
            configList.append(tmpConfig.copy())
            vertex = size
            row += 1
            offset = 0
    
    # print(configList)
    # for config in configList:
    #     print(config)
    return configList

# the following function will generate a graph of a given size
# graph can be of type: path or circle
def makeGraph(size, type):
    if size == 1:
        return {1:[1]}
    if size == 2:
        return {1:[2], 2:[1]}

    index = 1
    graph = {}
    edges = []
    while index < size+1:
        if index == 1 and type == 'path':
            edges.append(index+1)
        elif index == 1 and type == 'circle':
            edges.append(size)
            edges.append(index+1)
        elif index == size and type == 'path':
            edges.append(index-1)
        elif index == size and type == 'circle':
            edges.append(index-1)
            edges.append(1)
        else:
            edges.append(index-1)
            edges.append(index+1)
        
        kv = {index:edges}
        graph.update(kv)
        edges = []
        index += 1
    
    # print(graph)
    return graph
