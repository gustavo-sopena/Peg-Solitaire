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

Set these parameters to the desired value in main<span></span>.py.

### Example - Main

Suppose a game is played on a path graph with five vertices with three colors.

* `type`, `size`, `G`, and `C` are set as follows in main<span></span>.py
* `n` is set to the same value in main<span></span>.py and in game<span></span>.py
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

Suppose the same parameters are involved. This time, however, the configuration is not directly chosen.

First, in running configuration<span></span>.py, to indicate the desired parameters, pass them as arguments as shown in the example below.
Now, the program will play all configurations on the given graph.
That is, the program will build all possible arrangement of pegs based on the graph size and the number of colors chosen.
By using the `--range` argument, the program will play the specified subset of games.
Valid values are between `1` and `Total` (inclusive).

The total number of games can be referenced from the output of the `--dry-run` argument.
This will have the program simulate playing the game with the specified parameters and show possible results.

Finally, similar to the result in "example - main", if the games are winnable, then the generated excel file will contain the steps on how to win.

**Note:** If a parameter is omitted, then it will be set to a default value. For example, if the `--colorset` parameter is not specified, then internally, `n = 3`.

#### Results Screen

Here is the output when running configuration<span></span>.py.

```
$ python3 configuration.py --type path --size 5 --colorset 3
Generating File: ps-p(5)-z(3)-r[1-80].xlsx

Processing:
Configuration Section (1): Playing... Done.
Configuration Section (2): Playing... Done.
Configuration Section (3): Playing... Done.
Configuration Section (4): Playing... Done.
Configuration Section (5): Playing... Done.

Calculating Time... Done.
Saving xlsx File... Done.

Statistics:
Time: 0.000 hours = 0.000 minutes = 0.025 seconds
Total: 80
Played: 80
Won: 42
Lost: 38
Size: 5
Span: 16
Sections: 5
```
The generated excel file will contain the statistics from the output in the form of the table below.
|Total|Played|Won|Lost|Size|Span|Sections|Time (h)|Time (m)|Time (s)|
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|80|80|42|38|5|16|5|0.000|0.000|0.025|

* Total - the number of games available to play for the given graph size and the number of colors
* Played - the number of games played (obtained from `--range` or Total)
* Won - the number of games determined to be winnable
* Lost - the number of games determined to be not winnable
* Size - the number of vertices for the graph
* Span - the number of games per section
* Sections - the number of configuration sets (a group based on the graph size and the number of colors)
* Time - the number of hours, minutes, and seconds the program played the game

In addition, the file name is in a compact form by default.
Use the `-e` argument to switch to a descriptive form.

|Compact|Descriptive|
| --- | --- |
|`ps-p(5)-z(3)-r[1-80].xlsx`|`peg-solitaire-path(5)-colorset(3)-range[1-80].xlsx`|

#### Help

Use the `-h` or `--help` arguments for a view of all arguments.
```
$ python3 configuration.py --help
```

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

**Note:** Size is automatically calculated for a windmill and double star graph.

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

* As excel files are saved to the project directory, new excel files, added as a result from the program, will replace the old excel file

* As the number of colors and/or graph size increases, the program might take a long time to play a game or may not be able to play at all and throw a `RecursionError: maximum recursion depth exceeded in comparison` exception;
In running configuration<span></span>.py, if the error occurs, the program will safely exit, generating the excel file with any games played up to that point

* Increasing the number of recursions may cause python to use a lot of memory or cause other unforeseen issues

## Acknowledgments

* Dr. Matthew Rathbun, California State University, Fullerton
* Dr. Roberto Soto, California State University, Fullerton
