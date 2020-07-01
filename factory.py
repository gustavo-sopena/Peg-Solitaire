# name: factory
# description: Python Script that contains helper functions to play Peg Solitaire
# author: Gustavo Sopena
# date started: Friday: June 21, 2019

import math
import time
import contextlib

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

# the following function makes the format object for the excel file
def makeSheetCellFormat(workbook, *styles):
    style = {}
    for s in styles:
        style.update(s)
    return workbook.add_format(style)

# the following function finds all of the configurations for the given graph size and color set
# the output is a list of dictionaries
def findConfigurationsForGraphSizeAndColor(size, n, zeroPosition=1):
    tmpConfig = {}
    configList = []
    tmpList = []
    rowList = []

    # set row to 1
    # set vertex to the last vertex index in the graph
    # set maximum number of rows for the configuration
    row = 1
    vertex = size
    maxRows = math.pow(n-1, size-1)
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
        while vertex > 0: # loop over the number of vertices
            which = 1
            while row < printRows+1: # loop over each row
                which = which % n
                if which == 0:
                    which = 1

                # check how many times we have to print the current number
                index = 0
                while index < repeatFactor:
                    # print(listOneTwo[which])
                    tmpList.append(which)
                    index += 1
                
                # increase the row index
                row += 1
                which += 1
            
            # reduce the vertex by 1
            # reset the row to 1
            # double the repeat factor
            # half the number of max rows
            # save the temporary list into the master row list
            # reset the temporary list
            vertex -= 1
            row = 1
            repeatFactor *= n-1
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
            # increase the row index
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

# G = {1:[2, 3, 4, 5, 6, 7], 2:[1], 3:[1], 4:[1], 5:[1], 6:[1], 7:[1, 8, 9, 10, 11, 12], 8:[7], 9:[7], 10:[7], 11:[7], 12:[7]}
def makeDoubleStarGraph(leftSize, rightSize):
    if leftSize == 0 and rightSize == 0:
        return {1: [2], 2: [1]}

    root = 1
    graph = {}
    edges = []
    totalVertices = leftSize + rightSize + 2
    
    vertex = 1
    while vertex < totalVertices+1: # loop over all vertices
        if vertex == 1: # left root
            index = 2
            while index < leftSize+2+1: # loop through the number of vertices on the left side graph + 1 for right neighbor
                edges.append(index)
                index += 1
        elif vertex == leftSize + 2: # right root
            edges.append(1)
            index = leftSize + 2 + 1
            while index < leftSize+rightSize+2+1: # loop through the number of vertices on the left side graph + 1 for left neighbor
                edges.append(index)
                index += 1
            root = leftSize + 2
        else:
            edges = [root]
        
        kv = {vertex:edges}
        graph.update(kv)
        edges = []
        vertex += 1
    
    # print(graph)
    return graph

# the following function will generate windmill graphs
# the function takes as parameter the number of blades on the graph
def makeWindmillGraph(bladeCount):
    totalVertexCount = bladeCount * 2 + 1

    root = 1
    graph = {}
    edges = []
    
    vertex = 1
    while vertex < totalVertexCount+1: # loop over all vertices
        if vertex == 1: # root
            index = 2
            while index < totalVertexCount+1: # loop through the total number of vertices on the graph
                edges.append(index)
                index += 1
        elif vertex % 2 == 0: # even vertex
            edges = [root, vertex+1]
        elif vertex % 2 == 1: # even vertex
            edges = [root, vertex-1]
        
        kv = {vertex:edges}
        graph.update(kv)
        edges = []
        vertex += 1
    
    # print(graph)
    return graph

# the following function will time how long a block of code took to execute
# the time is logged to the results screen and to the excel file
@contextlib.contextmanager
def stopwatch(timesheet, align):
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        timesheet.write(0, 7, "Time (h)")
        timesheet.write(0, 8, "Time (m)")
        timesheet.write(0, 9, "Time (s)")
        timesheet.write(1, 7, "%.3f" % ((t1 - t0) / 3600), align)
        timesheet.write(1, 8, "%.3f" % ((t1 - t0) / 60), align)
        timesheet.write(1, 9, "%.3f" % (t1 - t0), align)
        print("Time: %.3f hours = %.3f minutes = %.3f seconds" % ((t1 - t0) / 3600, (t1 - t0) / 60, t1 - t0))
