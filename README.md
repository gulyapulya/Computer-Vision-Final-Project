# Dynamically measure objects in frame

## Short description
A webcam is pointed towards a background of known size. Any object that enters the background will have its contour identified and measured with length and width displayed in cm. The measurements dynamically follow the object.

## Dependencies:
- Python=3.8.5
- numpy
- opencv=4.0.1

## Instructions

Instructions to run the project is as follows:

- Clone/Download the repository from the main working branch.
- Navigate to the repo
- Run the python file `ObjectMeasurements.py` in an IDE or CLI.
- When running the file through a CLI, use the following lines:
    -    Running with still images, `python .\ObjectMeasurement.py`
    -    Running with webcam, `python .\ObjectMeasurement.py --camera `
- Point the camera at a piece of letter paper
- Make sure the letter paper is clear of any obstructions along its edges until a red border appears along the edge of the paper
- Place an item you wish to measure in the borders of the paper
- Press `q` to exit the program.   

## Sample usage 
<img width="262" alt="image" src="https://user-images.githubusercontent.com/54902370/231185627-7f309e89-6b94-43be-ba00-11e7bd23efaa.png">
<img width="263" alt="image" src="https://user-images.githubusercontent.com/54902370/231186415-b02fb8d1-7cf4-4c43-a732-11b37f60e7f9.png">
<img width="263" alt="image" src="https://user-images.githubusercontent.com/54902370/231186749-9c9fe36f-5b49-44d2-93c0-3ca8d470f3ec.png">

## Contributors: 
- Sunny [@sunnehh](https://github.com/sunnehh)
- Gulnur [@gulyapulya](https://github.com/gulyapulya)
- Suhail [@suhailsameer](https://github.com/suhailsameer)
