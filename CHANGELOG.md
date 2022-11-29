## [2.0.1]
* Fixed an issue with calculating the row and column width when the image has been resized to a square first.

## [2.0.0]
* [BREAKING] Swapped the rows and cols argument bindings in the script, as they were previously set incorrectly. Now `split-image test.jpg 3 2` will split the image into 3 rows and 2 columns (it previously split it into 3 columns and two rows). You may need to change your script arguments.
* Added the ability to batch process whole directories with images. Usage: `split-image image_dir 2 2` will split all images inside the `image_dir` folder. Closes #3.
* Fixed an issue with the image path name when it came from a directory.

## [1.7.0]
* Added the ability to set a `quiet` flag (`--quiet`), that will suppress all log messages (except errors and warnings) when running.

## [1.6.0]
* Can now import the package in your Python scripts with an import like `from split_image import split_image`.
* Fixed an issue with exporting squared (resized) JPG images.
* Refactored the `split` process to `split_image`.

## [1.5.1]
* Improved importing process for package

## [1.5.0]
* Added the ability to set a custom output directory for the image tiles. Usage: `split-image test.jpg 2 2 --output-dir <dir-name>`
