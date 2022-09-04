#!usr/bin/env python
import argparse
import os
import re
from collections import Counter

from PIL import Image


def split(im, rows, cols, image_path, should_cleanup):
    im_width, im_height = im.size
    row_width = int(im_width / rows)
    row_height = int(im_height / cols)
    n = 0
    for i in range(0, cols):
        for j in range(0, rows):
            box = (j * row_width, i * row_height, j * row_width +
                   row_width, i * row_height + row_height)
            outp = im.crop(box)
            name, ext = os.path.splitext(image_path)
            outp_path = name + "_" + str(n) + ext
            print("Exporting image tile: " + outp_path)
            outp.save(outp_path)
            n += 1
    if should_cleanup:
        print("Cleaning up: " + image_path)
        os.remove(image_path)


def reverse_split(paths_to_merge, rows, cols, image_path, should_cleanup):
    if len(paths_to_merge) == 0:
        print("No images to merge!")
        return
    for index, path in enumerate(paths_to_merge):
        path_number = int(path.split("_")[-1].split(".")[0])
        if path_number != index:
            print("Warning: Image " + path +
                  " has a number that does not match its index!")
            print("Please rename it first to match the rest of the images.")
            return
    images_to_merge = [Image.open(p) for p in paths_to_merge]
    image1 = images_to_merge[0]
    new_width = image1.size[0] * cols
    new_height = image1.size[1] * rows
    print(paths_to_merge)
    new_image = Image.new(image1.mode, (new_width, new_height))
    print("Merging image tiles with the following layout:", end=" ")
    for i in range(0, rows):
        print("\n")
        for j in range(0, cols):
            print(paths_to_merge[i * cols + j], end=" ")
    print("\n")
    for i in range(0, rows):
        for j in range(0, cols):
            image = images_to_merge[i * cols + j]
            new_image.paste(image, (j * image.size[0], i * image.size[1]))
    print("Saving merged image: " + image_path)
    new_image.save(image_path)
    if should_cleanup:
        for p in paths_to_merge:
            print("Cleaning up: " + p)
            os.remove(p)


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
                        help="The path of the image to process.")
    parser.add_argument("rows", type=int, default=2, nargs='?',
                        help="How many rows to split the image into (horizontal split).")
    parser.add_argument("cols", type=int, default=2, nargs='?',
                        help="How many columns to split the image into (vertical split).")
    parser.add_argument("-s", "--square", action="store_true",
                        help="If the image should be resized into a square before splitting.")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="Reverse the splitting process, i.e. merge multiple tiles of an image into one.")
    parser.add_argument("--cleanup", action="store_true",
                        help="After splitting or merging, delete the original image/images.")
    parser.add_argument("--load-large-images", action="store_true",
                        help="Ignore the PIL decompression bomb protection and load all large files.")
    args = parser.parse_args()
    image_path = args.image_path[0]
    if args.load_large_images:
        Image.MAX_IMAGE_PIXELS = None
    if args.reverse:
        print(
            "Reverse mode selected! Will try to merge multiple tiles of an image into one.")
        print("\n")
        start_name, ext = os.path.splitext(image_path)
        # Find all files that start with the same name as the image,
        # followed by "_" and a number, and with the same file extension.
        expr = re.compile(r"^" + start_name + "_\d+" + ext + "$")
        paths_to_merge = sorted([f for f in os.listdir(
            os.getcwd()) if re.match(expr, f)], key=lambda x: int(x.split("_")[-1].split(".")[0]))
        reverse_split(paths_to_merge, args.rows,
                      args.cols, image_path, args.cleanup)
    else:
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
            split(im_r, args.rows, args.cols, image_path, args.cleanup)
            print("Exporting resized image...")
            im_r.save(image_path + "_squared.png")
        else:
            split(im, args.rows, args.cols, image_path, args.cleanup)
    print("Done!")


if __name__ == "__main__":
    main()
