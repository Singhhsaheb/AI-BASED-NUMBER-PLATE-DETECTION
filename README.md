# AI-Based Number Plate Detection

This project uses **OpenCV** and **EasyOCR** to detect and recognize number plates from images of vehicles.

## Prerequisites

Python 3.7+ is recommended.
Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

Note: `easyocr` might require PyTorch. If you experience issues during installation or want GPU acceleration, please follow the [official PyTorch installation instructions](https://pytorch.org/get-started/locally/) before installing the requirements.

## Usage

Run the script from the command line, providing the path to an image as an argument:

```bash
python number_plate_detection.py <path_to_image.jpg>
```

### Example:

```bash
python number_plate_detection.py test_car.jpg
```

## Output

The script will print the detected text to the console and save a new image named `output_<original_name>.jpg` in the same directory, showing the detected bounding box and the read license plate text.
