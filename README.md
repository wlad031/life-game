Conway's Game of Life
===================

![preview](http://s011.radikal.ru/i315/1707/75/2111fa807fde.gif | height=256)   

Installation and running
-------------------------
 
 - Clone this repository:

```
git clone https://github.com/wlad031/life-game life-game
cd life-game/
```

 - Install python dependencies:

```
pip3 install -r requirements.txt
```

 - Install python-tk if it isn't installed

 - Run application:

```
python3 run.py
```

Configuration
-------------------------

Application configuration stored in ``preferences.cfg`` file. You can see an example and write your parameters.


Input
-------------------------

Application input file path can be configured by changing appropriate property in the config file.

Format of input file should be like this:
```
<i1> <j1>
<i2> <j2>
...
```
where ``ik`` and ``jk`` - coordinates of the alive cells.

``input.txt`` file contains example of the game configuration.
