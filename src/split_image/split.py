#!/usr/bin/env python
import argparse
import os
import re
from collections import Counter

from PIL import Image

def conditional_print(condition:bool, value, end=None):
    if not condition: return
    print(value, end=end)

def square_image(im: Image, should_quiet=False):
        im_width, im_height = im.size
        mode = im.mode
        min_dimension = min(im_width, im_height)
        max_dimension = max(im_width, im_height)
        conditional_print(not should_quiet, "Resizing image to a square...")
        conditional_print(not should_quiet, "Determining background color...")
        bg_color = determine_bg_color(im)
        conditional_print(not should_quiet, "Background color is... " + str(bg_color))
        im_r = Image.new(
            mode = mode,
            size = (max_dimension, max_dimension), 
            color = bg_color
            )
        offset = int((max_dimension - min_dimension) / 2)
        if im_width > im_height:
            im_r.paste(im, (0, offset))
        else:
            im_r.paste(im, (offset, 0))
        return im_r

def extract_tiles(im: Image, col_width: int, row_height: int):
    im_width, im_height = im.size 
    cols = im_width / col_width
    rows = im_height / row_height
    if not cols.is_integer(): raise ValueError("column width must be a factor of the total image width")
    if not rows.is_integer(): raise ValueError("row height must be a factor of the total image height")
    rows, cols = int(rows), int(cols)
    outputs = []
    for i in range(0, rows):
        for j in range(0, cols):
            box = (j * col_width, i * row_height, j * col_width +
                   col_width, i * row_height + row_height)
            outputs.append(im.crop(box))
    return outputs

def split_image(image_path, rows, cols, should_square, should_cleanup, should_quiet=False, output_dir=None):
    im = Image.open(image_path)
    im_width, im_height = im.size
    col_width = int(im_width / cols)
    row_height = int(im_height / rows)
    name, ext = os.path.splitext(image_path)
    name = os.path.basename(name)
    if output_dir != None:
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = "./"
    if should_square:
        im_r = square_image(im, should_quiet)
        conditional_print(not should_quiet, "Exporting resized image...")
        outp_path = name + "_squared" + ext
        outp_path = os.path.join(output_dir, outp_path)
        im_r.save(outp_path) # intermediary file output
        im = im_r
        col_width = int(im.size[0] / cols)
        row_height = int(im.size[1] / rows)

    outputs = extract_tiles(im, col_width, row_height)

    for n, item in enumerate(outputs):
        outp_path = name + "_" + str(n) + ext
        outp_path = os.path.join(output_dir, outp_path)
        conditional_print(not should_quiet, "Exporting image tile: " + outp_path)
        item.save(outp_path) # final file outputs
    if should_cleanup:
        conditional_print(not should_quiet, "Cleaning up: " + image_path)
        os.remove(image_path)

def reverse_split(paths_to_merge, rows, cols, image_path, should_cleanup, should_quiet=False):
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
    new_image = Image.new(image1.mode, (new_width, new_height))
    for path in paths_to_merge:
        conditional_print(not should_quiet, path)
    conditional_print(not should_quiet, "Merging image tiles with the following layout:", end=" ")
    for i in range(0, rows):
        print("\n")
        for j in range(0, cols):
            print(paths_to_merge[i * cols + j], end=" ")
    print("\n")
    for i in range(0, rows):
        for j in range(0, cols):
            image = images_to_merge[i * cols + j]
            new_image.paste(image, (j * image.size[0], i * image.size[1]))
    conditional_print(not should_quiet, "Saving merged image: " + image_path)
    new_image.save(image_path)
    if should_cleanup:
        for p in paths_to_merge:
            conditional_print(not should_quiet, "Cleaning up: " + p)
            os.remove(p)

def determine_bg_color(im, border_percentage: int = 5):
    if not (0 <= border_percentage <= 100): raise ValueError("border_percentage must be between 0 and 100")
    rgb_im = im.convert('RGBA')
    width, height = im.size
    border_px_width = int(width * border_percentage / 100)
    border_px_height = int(height * border_percentage / 100)
    edges = []
    edges.extend(rgb_im.crop((0, 0, width, border_px_height)).get_flattened_data())
    edges.extend(rgb_im.crop((0, 0, border_px_width, height)).get_flattened_data())
    edges.extend(rgb_im.crop((width - border_px_width, 0, width, height)).get_flattened_data())
    edges.extend(rgb_im.crop((0, height - border_px_height, width, height)).get_flattened_data())
    
    return Counter(edges).most_common(1)[0][0]

def main():
    parser = argparse.ArgumentParser(
        description="Split an image into rows and columns.")
    parser.add_argument("image_path", nargs=1,
                        help="The path to the image or directory with images to process.")
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
    parser.add_argument("--output-dir", type=str,
                        help="Set the output directory for image tiles (e.g. 'outp/images'). Defaults to current working directory.")
    parser.add_argument("--quiet", action="store_true",
                        help="Run without printing any messages.")

    args = parser.parse_args()
    if args.load_large_images:
        Image.MAX_IMAGE_PIXELS = None
    image_path = args.image_path[0]
    if not os.path.exists(image_path):
        print("Error: Image path does not exist!")
        return
    if os.path.isdir(image_path):
        if args.reverse:
            print("Error: Cannot reverse split a directory of images!")
            return
        conditional_print(not args.quiet, "Splitting all images in directory: " + image_path)
        for file in os.listdir(image_path):
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                split_image(os.path.join(image_path, file), args.rows, args.cols,
                            args.square, args.cleanup, args.quiet, args.output_dir)
    else:
        if args.reverse:
            conditional_print(not args.quiet, "Reverse mode selected! Will try to merge multiple tiles of an image into one.\n")
            start_name, ext = os.path.splitext(image_path)
            # Find all files that start with the same name as the image,
            # followed by "_" and a number, and with the same file extension.
            expr = re.compile(r"^" + start_name + "_\d+" + ext + "$")
            paths_to_merge = sorted([f for f in os.listdir(
                os.getcwd()) if re.match(expr, f)], key=lambda x: int(x.split("_")[-1].split(".")[0]))
            reverse_split(paths_to_merge, args.rows,
                          args.cols, image_path, args.cleanup, args.quiet)
        else:
            split_image(image_path, args.rows, args.cols,
                        args.square, args.cleanup, args.quiet, args.output_dir)
    conditional_print(not args.quiet, "Done!")


if __name__ == "__main__":
    main()
