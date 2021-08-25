# split-image


## Quickly split an image into rows and columns (tiles).

[split-image](https://pypi.org/project/split-image/) is a Python package that you can use from the command line to split an image into tile.

## Installation


`pip install split-image`

## Usage

From the command line:

`split-image [-h] [-s] image_path rows cols`

### Basic examples

`split-image test.png 2 2`

This splits the `test.png` image in 4 tiles (`2` rows and `2` columns)

`split-image test.png 3 4 -s`

This splits the `test.png` image in 12 tiles (`3` rows and `4` columns). The `-square` arguments resizes the image into a square before splitting it. 


```

positional arguments:
  image_path    The path of the image to split.
  rows          How many rows to split the image into (horizontal split).
  cols          How many columns to split the image into (vertical split).

optional arguments:
  -h, --help    show this help message and exit
  -s, --square  If the image should be resized into a square before splitting.


```

