#!usr/bin/env python

import argparse
from collections import Counter

from PIL import Image


def split(im, rows, cols, image_path):
    im_width, im_height = im.size
    row_width = int(im_width / rows)
    row_height = int(im_height / cols)
    n = 0
    for i in range(0, cols):
        for j in range(0, rows):
            box = (j * row_width, i * row_height, j * row_width +
                   row_width, i * row_height + row_height)
            print(box)
            outp = im.crop(box)
            outp_path = image_path.split(".")[0] + "_" + str(n) + ".png"
            print("Exporting image tile: " + outp_path)
            outp.save(outp_path)
            n += 1


def determine_bg_color(im):
    print("Determining background color...")
    im_width, im_height = im.size
    rgb_im = im.convert('RGBA')
    all_colors = []
    areas = [[(0, 0), (im_width, im_height / 10)],
             [(0, 0), (im_width / 10, im_height)],
             [(im_width * 9 / 10, 0), (im_width, im_height)],
             [(0, im_height * 9 / 10), (im_width, im_height)]]
    for area in areas:
        start = area[0]
        end = area[1]
        for x in range(int(start[0]), int(end[0])):
            for y in range(int(start[1]), int(end[1])):
                pix = rgb_im.getpixel((x, y))
                all_colors.append(pix)
    return Counter(all_colors).most_common(1)[0][0]


def main():
    parser = argparse.ArgumentParser(
        description="Split an image into rows and columns.")
    parser.add_argument("image_path", nargs=1,
                        help="The path of the image to split.")
    parser.add_argument("rows", type=int, default=2,
                        help="How many rows to split the image into (horizontal split).")
    parser.add_argument("cols", type=int, default=2,
                        help="How many columns to split the image into (vertical split).")
    parser.add_argument("-s", "--square", action="store_true",
                        help="If the image should be resized into a square before splitting.")
    args = parser.parse_args()
    image_path = args.image_path[0]
    im = Image.open(image_path)
    im_width, im_height = im.size
    min_dimension = min(im_width, im_height)
    max_dimension = max(im_width, im_height)

    if args.square:
        print("Resizing image to a square...")
        bg_color = determine_bg_color(im)
        print("Background color is... " + str(bg_color))
        im_r = Image.new("RGBA", (max_dimension, max_dimension), bg_color)
        offset = int((max_dimension - min_dimension) / 2)
        if im_width > im_height:
            im_r.paste(im, (0, offset))
        else:
            im_r.paste(im, (offset, 0))
        split(im_r, args.rows, args.cols, image_path)
        print("Exporting resized image...")
        im_r.save(image_path + "_squared.png")
    else:
        split(im, args.rows, args.cols, image_path)
    print("Done!")


if __name__ == "__main__":
    main()
