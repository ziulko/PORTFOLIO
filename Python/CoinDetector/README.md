# Coin Tray Analyzer

A computer vision program using OpenCV that detects and classifies coins placed on a tray in an image. It distinguishes between 5 zł and 0.05 zł coins, determines whether they're inside or outside a detected tray boundary, and estimates total value and surface areas.

> This project is a prototype and is not guaranteed to work on all images. Accuracy depends heavily on image quality, contrast, and consistent coin size.

## Features

- Detect tray boundaries using Hough Line Transform
- Detect circular coins using Hough Circle Transform
- Classify coins as 5 zł or 0.05 zł based on radius
- Distinguish between coins inside vs outside the tray
- Calculate:
  - Total value of coins
  - Area covered by coins
  - Tray coverage
- Visual display of results with overlay

## Example Output
5 zł coins inside tray: 3 \
5 zł coins outside tray: 1 \
0.05 zł coins inside tray: 2 \
0.05 zł coins outside tray: 0 \
Total inside tray: 15.1 zł\
Total outside tray: 5.0 zł\
Total value: 20.1 zł

Tray area: 215664 px²\
Single 5 zł coin area (example): 3058.11 px²\
5 zł coin is 1.4180% the size of the tray.


## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- NumPy

## Usage

Place your coin tray image in the pliki/ folder. Update the image_path in the main() function:

image_path = 'pliki/tray7.jpg'\
Run the program:

python coin_detector.py
## To Do

Improve classification thresholds using training data
Add GUI for selecting image
Auto-scale detection based on image resolution
