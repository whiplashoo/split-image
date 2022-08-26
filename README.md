# split-image

[![Downloads](https://static.pepy.tech/personalized-badge/split-image?period=total&units=international_system&left_color=blue&right_color=orange&left_text=Downloads)](https://pepy.tech/project/split-image) [![Downloads](https://static.pepy.tech/personalized-badge/split-image?period=month&units=international_system&left_color=blue&right_color=yellow&left_text=Downloads%20per%20month)](https://pepy.tech/project/split-image)

## Quickly split an image into rows and columns (tiles).

[split-image](https://pypi.org/project/split-image/) is a Python package that you can use from the command line to split an image into tiles.

<p align="center">
<img width="75%" src="https://user-images.githubusercontent.com/9117427/130825947-e78c4d15-6a89-40f8-9aa1-ddfa3b23779c.png"/>
</p>

## Installation


`pip install split-image`

## Usage

From the command line:

`split-image [-h] [-s] image_path rows cols`

<p align="center">
<img width="75%" src="https://user-images.githubusercontent.com/9117427/130827013-1dfe300c-9a2d-4b44-a27b-86a6781e115b.png"/>
</p>

### Basic examples

`split-image cat.png 2 2`

This splits the `cat.png` image in 4 tiles (`2` rows and `2` columns).

<p align="center">
<img width="75%" src="https://user-images.githubusercontent.com/9117427/130825960-4db37eb7-08e0-467e-8f30-fcfd38cad732.png"/>
</p>

`split-image bridge.png 3 4 -s`

This splits the `bridge.png` image in 12 tiles (`3` rows and `4` columns). The `-square` arguments resizes the image into a square before splitting it. The background color used to fill the square is determined from the image automatically.

<p align="center">
<img width="75%" src="https://user-images.githubusercontent.com/9117427/130825967-f191a5d9-c5c6-4ee3-9dbe-5943a40725fd.png"/>
</p>

### Other options

#### Reverse split:

`split-image cat.jpg 2 2 -r`

Will attempt to merge similarly named image tiles to one image. So, if you have these images in the current directory:

* `cat_0.jpg`
* `cat_1.jpg`
* `cat_2.jpg`
* `cat_3.jpg`

they will be merged according to their file name:

<p align="center">
<img width="75%" src="https://user-images.githubusercontent.com/9117427/182033564-514a47c9-f76e-4ee7-9520-7b1dac68f221.png"/>
</p>

#### Cleanup:

`split-image test.jpg 4 2 --cleanup`

Will delete the original image after the process.

#### Large images:

`split-image test.jpg 4 2 --load-large-images`

When working with large images (over 178,956,970 pixels), you may get an error. Pass this flag to override this.

```

positional arguments:
  image_path    The path of the image to split.
  rows          How many rows to split the image into (horizontal split).
  cols          How many columns to split the image into (vertical split).

optional arguments:
  -h, --help            Show this help message and exit
  -s, --square          If the image should be resized into a square before splitting.
  -r, --reverse         Reverse the splitting process, i.e. merge multiple tiles of an image into one.
  --cleanup             After splitting or merging, delete the original image/images.
  --load-large-images   Pass this flag for use with really large images.

```

Cat photo by <a href="https://unsplash.com/@madhatterzone?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Manja Vitolic</a> on <a href="https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  
Bridge photo by <a href="https://unsplash.com/@lance_asper?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Lance Asper</a> on <a href="https://unsplash.com/s/photos/bridge?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>


