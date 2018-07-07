# Pytris_TGM

This is a python implementation of [Tetris](https://en.wikipedia.org/wiki/Tetris) using the [TGM](https://en.wikipedia.org/wiki/Tetris:_The_Grand_Master) [ruleset](http://tetris.wikia.com/wiki/Tetris_The_Grand_Master).

## TODO List

- [x] Package up code to be used with pip install
- [x] Add pygame display functionality
- [ ] Compartmentalize pygame display functionality
- [ ] Add support for [OpenAI Gym](https://gym.openai.com/) interface
- [ ] Complete README documentation
- [ ] Add automated testing
- [ ] Add seed for randomization
- [ ] Make tetronimos into a class

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prequisites

Pytris requires at least Python 3.6 and these libraries:

```Shell
pip install pygame
```

### Installing

To install Pytris, clone the repository and call pip:

```Shell
git clone https://github.com/mpberk/pytris_tgm.git
cd ./pytris_tgm
pip install -e .
```

### Running

To run Pytris, call the following:

```Shell
python ./pytris_tgm/pytris_tgm_display_pygame.py
```

Or call the following in a python script:

```Python
from pytris_tgm import PytrisTGMDisplay

pytris = PytrisTGMDisplay()
pytris.start()
```

## Controls

To control Pytris, use the following controls:

* Left Key
* Right Key
* Down Key
* Z - A Rotate
* X - B Rotate
* C - C Rotate

## Authors

* **Matt Berk** - *Initial work* - [https://github.com/mpberk](https://github.com/mpberk)

See also the list of [contributors](https://github.com/mpberk/pytris_tgm/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
