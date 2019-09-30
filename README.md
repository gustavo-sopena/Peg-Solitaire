# Peg Solitaire

This project is an implementation of peg solitaire in python with some modifications. In this project, pegs are colored arbitrarily from a finite set of colors labeled as integer values. The objective is to have one peg remaining irrespective of the color of the peg after a series of moves. That is, pegs can jump over other pegs into an empty vertex on a graph provided that the vertices they occupy are connected to one another. Depending on the color of the pegs involved, pegs can either change into another peg of a different color or are removed.

## Getting Started

On macOS, check if python 3 is installed by typing into terminal:
```
$ which python3
```
If nothing is displayed after running the command, then download and install [python 3](https://www.python.org/downloads/).

Afterwards, install the python module used to create excel files with:
```
$ pip3 install xlsxwriter
```

## Playing Games

The following parameters are used to play the game.

* `n` - the number of colors, set as an integer

    The colors are labeled as 0, 1, 2, ..., `n`-1. The color 0 represents an empty vertex where pegs move into.

* `size` - the number of vertices for the graph, set as an integer
* `type` - the name of the graph under consideration, set as a string
* `G` - the graph definition

    Graphs are set as a dictionary with the keys as integers representing vertices and the values as lists of integers representing the vertices connected to the current vertex.

    For example,
    ```
    G = {1:[2], 2:[1, 3], 3:[2]}
    ```
    This is a path graph that is composed of three vertices. The first vertex is connected to the second vertex. The second vertex is connected to the first vertex and the third vertex. Finally, the third vertex is connected to the second vertex.

* `C` - the configuration of the pegs

    Configurations are set as a dictionary with the keys as integers representing vertices and the values as integers representing pegs of a certain color.

    For example,
    ```
    C = {1:0, 2:1, 3:1}
    ```
    This is a configuration in which vertices two and three contain a peg of color 1 and vertex one is empty.

    **Note:** `C` is defined to have one empty vertex and is usually the first vertex.

Set these parameters to the desired value in either main<span></span>.py or configuration<span></span>.py.

### Example - Main

Suppose a game is played on a path graph with five vertices with three colors.

* `type`, `size`, `G`, and `C` are set as follows in main<span></span>.py
* `n` is set to the same value in main<span></span>.py and in PegGame<span></span>.py
```
n = 3
size = 5
type = 'path'
G = {1:[2], 2:[1, 3], 3:[2, 4], 4:[3, 5], 5:[4]}
C = {1:0, 2:1, 3:1, 4:1, 5:1}
```
Running the file produces the following result.
```
$ python3 main.py
Saving to file: peg-solitaire-example-sheet-path-5-z3.xlsx
Win: True
0 1 1 1 1
1 2 0 1 1
0 0 1 1 1
0 1 2 0 1
0 0 0 1 1
0 0 1 2 0
0 0 0 0 1
```
If the game is winnable, as in this case, then the resulting excel file will contain the steps on how to win.

**Note:** PlayPegGame<span></span>.py contains more graphs and their configuration.

### Example - Configuration

Suppose the same parameters are involved. This time, however, the configuration is not chosen.

The program will play all configurations on the given graph. That is, the program will find all possible arrangement of pegs based on the number of colors chosen. To indicate the desired parameters, pass them as arguments when running the file.
```
$ python3 configuration.py --type path --size 5 --colorset 3
Saving to file: peg-solitaire-configuration-sheet-path-5-z3.xlsx
Total: 80
Played: 80
Won: 42
Lost: 38
```
Similar to the result in "example - main", if the games are winnable, then the resulting excel file will contain the steps on how to win.

Use the `-h` or `--help` arguments for a compact view of the parameters.
```
$ python3 configuration.py --help
```
**Note:** If a parameter is omitted, then it will be set to a default value. For example, if the `--colorset` parameter is not specified, then internally, `n = 3`.

### Graphs

Graphs are made by using the appropriate function from factory<span></span>.py:

* `makeGraph(size, type)` function for a path or circle graph
* `makeWindmillGraph(bladeCount)` function for a windmill graph
* `makeDoubleStarGraph(leftSize, rightSize)` function for a double star graph

For example,
```
size = 10
type = 'path'
G = factory.makeGraph(size, type)
```
This creates a path graph with ten vertices.

**Note:** `size` is automatically calculated for a windmill and double star graph.

## Contributing

If you want to contribute:

* Fork this repository and create a local clone
* Develop your edits in a new branch and commit
* Push your commit to your fork

Then, submit a pull request!

## TODO

### Features

* Build a family of "make graph" functions by adding the ability to make:

    * Tree Graphs
    * (Complete) Bipartite Graphs

### Bugs + Issues

* As excel files are saved to the project directory, new excel files with the same name as a file already in the directory will replace the old excel file

* As the number of colors and/or graph size increases, the program might take a long time to play a game or may not be able to play at all and show a `RecursionError: maximum recursion depth exceeded in comparison` message;
When running configuration<span></span>.py, the `--limit` option can be used to increase the number of recursions

## Acknowledgments

* Dr. Matthew Rathbun, California State University, Fullerton
* Dr. Roberto Soto, California State University, Fullerton
