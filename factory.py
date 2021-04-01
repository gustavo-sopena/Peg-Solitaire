# name: factory
# description: Python Script that contains helper functions to play Peg Solitaire
# author: Gustavo Sopena
# date started: Friday: June 21, 2019

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

# the following function builds all of the configurations for the given graph size and color set
def buildConfigurations(size, n, zero=1, alpha=0, beta=0):
    if size <= 1:
        return {1:0}

    tmpConfig = {}
    configList = []
    tmpList = []
    rowList = []

    # set current vertex to the last vertex in the graph
    # set maximum number of games
    # build all of the configurations if alpha and beta are not specified
    vertex = size
    games = (n-1) ** (size-1)
    alpha = 1 if alpha == 0 or alpha < 0 else alpha
    beta = games if beta == 0 or beta > games else beta
    alpha = 1 if alpha > beta else alpha
    beta = games if alpha > beta else beta

    # print("size: {}".format(size))
    # print("colorset: {}".format(n))
    # print("zero position: {}".format(zero))
    # print("games: {}".format(games))
    # print("alpha: {}".format(alpha))
    # print("beta: {}".format(beta))

    # size >= 2
    repeatFactor = 1
    repeatIndex = 0

    # loop over each vertex, then loop over each row
    while vertex > 1:
        color = 1
        for row in range(1, beta+1):
            color = 1 if color % n == 0 else color
            if row >= alpha:
                tmpList.append(color)

            color = color if repeatIndex < repeatFactor-1 else color+1
            repeatIndex = repeatIndex+1 if repeatIndex < repeatFactor-1 else 0
            repeatIndex = 0 if row == beta else repeatIndex

        vertex -= 1
        repeatFactor *= n-1
        rowList.append(tmpList)
        tmpList = []

    # loop over each row, then loop over each vertex
    for row in range(1, beta-alpha+1+1):
        offset = 1
        for vertex in range(1, size+1):
            if vertex == zero:
                offset = 0
                tmpConfig[vertex] = 0
            else:
                tmpConfig[vertex] = rowList[size-vertex-offset][row-1]

        configList.append(tmpConfig.copy())

    return configList

# the following function generates a path graph
# the second argument specifies the index to which the graph starts labeling
def makePathGraph(size, start=1):
    if size == 1:
        return {start:[start+1], start+1:[start]}

    vertex = start
    graph = {}
    edges = []
    while vertex < start+size:
        if vertex == start:
            edges.append(vertex+1)
        elif vertex == start+size-1:
            edges.append(vertex-1)
        else:
            edges.append(vertex-1)
            edges.append(vertex+1)

        kv = {vertex:edges}
        graph.update(kv)
        edges = []
        vertex += 1

    # print(graph)
    return graph

# the following function generates a circle graph
def makeCircleGraph(size, start=1):
    if size == 1 or size == 2:
        return {start:[start+1], start+1:[start]}

    graph = makePathGraph(size, start)

    graph[start].append(size+start-1)
    graph[size+start-1].append(start)

    # print(graph)
    return graph

# the folllowing function generates a complete graph
def makeCompleteGraph(size, start=1):
    graph = makeCircleGraph(size, start)

    # connect each vertex on the circle to one another
    vertex = start
    connectVertex = 3 + (start - 1)
    diagonals = size - 3

    if diagonals > 0:
        while vertex < size+start:
            for s in range(0, diagonals):
                graph[vertex].append(connectVertex)
                connectVertex += 1
                connectVertex = start if connectVertex == (size+start) else connectVertex

            for s in range(0, size-4):
                connectVertex -= 1
                connectVertex = size+start-1 if connectVertex == (start-1) else connectVertex

            vertex += 1

    # print(graph)
    return graph

# the following function generates a double star graph
def makeDoubleStarGraph(leftSize, rightSize, start=1):
    if leftSize == 0 and rightSize == 0:
        return {1: [2], 2: [1]}

    graph = {}
    edges = []
    totalVertices = leftSize + rightSize + 2

    vertex = start
    while vertex < totalVertices+start: # loop over all vertices
        if vertex == start: # left root
            index = start+1
            while index < start+leftSize+2: # loop through the number of vertices on the left side graph + 1 for right neighbor
                edges.append(index)
                index += 1
            root = start
        elif vertex == start+leftSize+1: # right root
            edges.append(start)
            index = start+leftSize+2
            while index < start+leftSize+rightSize+2: # loop through the number of vertices on the left side graph + 1 for left neighbor
                edges.append(index)
                index += 1
            root = start+leftSize+1
        else:
            edges = [root]

        kv = {vertex:edges}
        graph.update(kv)
        edges = []
        vertex += 1

    # print(graph)
    return graph

# the following function will generates a windmill graph
# the function takes as parameter the number of blades on the graph
def makeWindmillGraph(bladeCount, start=1):
    totalVertexCount = bladeCount * 2 + 1

    isOdd = True if start % 2 == 1 else False
    graph = {}
    edges = []
    
    vertex = start
    while vertex < totalVertexCount+start: # loop over all vertices
        if vertex == start: # root
            index = start+1
            while index < totalVertexCount+start: # loop through the total number of vertices on the graph
                edges.append(index)
                index += 1
        elif vertex % 2 == 0: # even vertex
            edges = [start, vertex+1 if isOdd else vertex-1]
        elif vertex % 2 == 1: # odd vertex
            edges = [start, vertex-1 if isOdd else vertex+1]
        
        kv = {vertex:edges}
        graph.update(kv)
        edges = []
        vertex += 1
    
    # print(graph)
    return graph

# the following function generates a caterpillar graph
def makeCaterpillarGraph(pendants, start=1):
    size = len(pendants)
    graph = makePathGraph(size, start)

    index = size+start-1
    for vertex in range(start, size+start):
        for i in range(1, pendants[vertex-start] + 1):
            index += 1
            graph[vertex].append(index)
            kv = {index:[vertex]}
            graph.update(kv)

    # print(graph)
    return graph

# the following function generates a lollipop graph
def makeLollipopGraph(completeSize, stemSize, start=1):
    if completeSize == 1 and stemSize == 1:
        return {start: [start+1], start+1: [start]}

    complete = makeCompleteGraph(completeSize, start)

    if stemSize == 0:
        return complete

    path = makePathGraph(stemSize, completeSize+start)

    # remove the extra node on the complete graph or path graph on size one
    if completeSize == 1:
        complete.pop(start+1)
    if stemSize == 1:
        path.pop(completeSize+start+1)
        path[completeSize+start].remove(completeSize+start+1)

    # do not append an extra node to the first node on size one
    if completeSize != 1:
        complete[start].append(completeSize+start)

    path[completeSize+start].append(start)

    graph = {**complete, **path}

    # print(graph)
    return graph

# the following function generates a house graph
def makeHouseGraph(start=1):
    graph = makeCircleGraph(5, start)

    graph[start+4].append(start+1)
    graph[start+1].append(start+4)

    # print(graph)
    return graph

# the following function generates a house x-graph
def makeHouseXGraph(start=1):
    graph = makeCircleGraph(5, start)

    graph[start+4].append(start+1)
    graph[start+1].append(start+4)

    graph[start+1].append(start+3)
    graph[start+3].append(start+1)

    graph[start+2].append(start+4)
    graph[start+4].append(start+2)

    # print(graph)
    return graph

# the following function generates a grid graph
def makeGridGraph(row, column, start=1):
    if row == 1 or column == 1:
        raise ValueError

    graph = {}

    pRow = None
    cRow = None

    # create the variable that we can use to update the vertex label for each row
    vertexUpdate = column

    # create the first row
    mRow = makePathGraph(column, start)

    # add the first row to the graph
    graph.update(mRow)

    # loop over the row count
    for i in range(2, row+1):
        # set the previous row to the first row
        if i == 2:
            pRow = mRow
        else:
            pRow = cRow

        cRow = makePathGraph(column, start+vertexUpdate)

        # loop over the column count
        for v in cRow:
            cRow[v].append(v-column)
            pRow[v-column].append(v)

        vertexUpdate += column

        graph.update(cRow)

    # print(graph)
    return graph

# the following function generates a mongolian tent graph
def makeMongolianTentGraph(row, column, start=1):
    if row < 2 or column < 3:
        raise ValueError("grid size cannot be smaller than a 2 x 3")
    if column % 2 == 0:
        raise ValueError("column integer {} cannot be even".format(column))

    graph = makeGridGraph(row, column, start+1)

    # the extra vertex (vertex "start") connects to every other vertex starting from the first one of the first row
    vertex = {start:[]}

    for v in range(start+1, column+start+1, 2):
        vertex[start].append(v)
        graph[v].append(start)

    graph.update(vertex)

    # print(graph)
    return graph

# the following function gets an integer between begin and end
# after traversing a certain number of steps either forwards or backwards
def getListVertex(vertex, begin, end, step):
    value = vertex + step

    if value <= begin-1:
        distance = begin - value - 1
        value = end - distance
    elif value >= end+1:
        distance = end - value + 1
        value = begin - distance

    return value

# the following function generates a generalized petersen graph
def makeGeneralizedPetersenGraph(size, step, start=1):
    if size < 3:
        raise ValueError("Size must be greater than or equal to 3")

    upperStepBound = int((size - 1) / 2)
    if (step < 1) or (step > upperStepBound):
        raise ValueError("This value must be an integer value between [1, {}] inclusive".format(upperStepBound))

    inner = None
    outer = makeCircleGraph(size, start)

    if step == 1:
        inner = makeCircleGraph(size, start+size)
    else:
        inner = {}
        vertex = start + size
        while vertex < start+2*size:
            # create a list containing two values obtained by counting forwards and backwards in the graph by the step size
            edge = [getListVertex(vertex, start+size, start+size+size-1, step), getListVertex(vertex, start+size, start+size+size-1, -step)]
            inner.update({vertex:edge})
            edge = []
            vertex += 1

    # connect the outer vertices to the inner vertices
    for v in outer:
        outer[v].append(v+size)
        inner[v+size].append(v)

    graph = {**inner, **outer}

    # print(graph)
    return graph

# the following function generates a barbell graph
def makeBarbellGraph(bellSize, start=1):
    leftBell = makeCompleteGraph(bellSize, start)
    rightBell = makeCompleteGraph(bellSize, bellSize+start)

    leftBell[start].append(bellSize+start)
    rightBell[bellSize+start].append(start)

    graph = {**leftBell, **rightBell}

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
