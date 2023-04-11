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
- Run the python file `ObjectMeasurements.py` in an IDE or CLI.
- When running the file through a CLI, use the following lines:
    -    Running with still images, `python .\ObjectMeasurement.py`
    -    Running with webcam, `python .\ObjectMeasurement.py --camera `
- Point the camera at a piece of letter paper
- Make sure the letter paper is clear of any obstructions along its edges until a red border appears along the edge of the paper
- Place an item you wish to measure in the borders of the paper
- Press `q` to exit the program.   

## Contributors: 
- Sunny [@sunnehh](https://github.com/sunnehh)
- Gulnur [@gulyapulya](https://github.com/gulyapulya)
- Suhail [@suhailsameer](https://github.com/suhailsameer)


## Instructions

Requirements: python3, opencv, numpy.


- Clone the repo on your local machine 
- Navigate to the repo
- Define your camera settings in the config.py file, if using video from a webcam
- Change webcam variable to True or False in ObjectMeasurement.py depending if you use a webcam or no  
- If not using the camera, change image_path variable in ObjectMeasurement.py to the preffered sample image
- Build and run ObjectMeasurement.py
``python ObjectMeasurement.py``

## Sample usage 
<img width="262" alt="image" src="https://user-images.githubusercontent.com/52351598/231058044-5f9afbba-ffdc-46b3-9044-606553eaacb0.png">
<img width="262" alt="image" src="https://user-images.githubusercontent.com/52351598/231058076-034e06b5-f30c-42d6-b00f-3bc337c0bab9.png">
<img width="263" alt="image" src="https://user-images.githubusercontent.com/52351598/231058098-b0c0d2f5-d717-4b34-99b5-f0fe1758d290.png">
