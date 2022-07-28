# Rectify stereo images

Python code to rectify a left-right stereo image pair.

## Usage

```sh
recitify.py [-h] [--left LEFT] [--right RIGHT] [--output [OUTPUT]] [--alpha [ALPHA]] [--debug]

options:
  -h, --help         show this help message and exit
  --left LEFT        Path to left image
  --right RIGHT      Path to right image
  --output [OUTPUT]  Path to output image. Default: rectified_pair.png
  --alpha [ALPHA]    Alpha value for rectification. Default: 0.0
  --debug            Save debug RGB images and show epipolar lines
```

## Example

For standard rectification:
```sh
python recitify.py --left L.png --right R.png
```

For standard rectification with debug files and epipolar lines
```sh
python recitify.py --left L.png --right R.png --debug
```

For rectification with a different alpha value
```sh
python recitify.py --left L.png --right R.png --alpha 0.66
```

To change the output filename

```sh
python recitify.py --left L.png --right R.png --output my_new_filename.png
```