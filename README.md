<h1 align="center">
  <br>
    <img src="https://i.ibb.co/Gfq6n7K3/robocat-logo.png" alt="RoboCat Logo" width="250">
  <br>
    RoboCat
  <br>
</h1>

<h4 align="center">A quadruped robot developed by third-year Computer Science students at the Universitat Autònoma de Barcelona.</h4>

<p align="center">
  <!----------------------- UAB | Robótica ----------------------->
  <a href="https://rlpengineeringschooluab.wordpress.com"><img src="https://img.shields.io/badge/UAB-RLP-3FB911" alt="UAB | RLP"></a>
  <!--------------------------- Status --------------------------->
  <img src="https://img.shields.io/badge/status-prototype-4CB696" alt="Status | Prototype">
  <!---------------------------  Raspi --------------------------->
  <a href="https://www.raspberrypi.com/">
  <img src="https://img.shields.io/badge/-Raspberry%20Pi-A22846?logo=Raspberry%20Pi&logoColor=white" alt="Raspberry Pi Badge"></a>
  <!--------------------------- THX U ---------------------------->
  <img alt="Thank You <3!" src="https://img.shields.io/badge/%3C3-Thank_you!-blue">
  
</p>

 <!---Modificar per els nostres casos--->
<p align="center">
  <a href="#What-is-RoboCat">What is RoboCat?</a> •
  <a href="#Requirements">Requirements</a> •
  <a href="#How-To-Use">How to use</a> •
  <a href="#Components">Components</a> •
  <a href="#Software">Software</a> •
  <a href="#Tech-Stack">Tech Stack</a> •
  <a href="#License">License</a> •
  <a href="#Contribution">Contribution</a> •
  <a href="#Credits">Credits</a>
</p>

![screenshot](https://raw.githubusercontent.com/joanmarc28/Robocat/main/gallery/model_360.gif)


# What is RoboCat?

RoboCat is an autonomous quadruped robot designed to patrol public streets and monitor parking zones that are regulated by payment. Its structure and external appearance is inspired by the shape of a cat, making it not only functional but also friendly and approachable for pedestrians.
Equipped with sensors, cameras and onboard computing, RoboCat can detect whether a parked vehicle has an active parking permit or not, combining robotics, computer vision and real-time data processing to offer a smart, mobile solution for urban mobility enforcement.

The project main goals are to:
  - Automate parking control in regulated areas
  - Reduce the need for manual inspection
  - Integrate urban robotics with a friendly and non-threatening design
  - Demonstrate the application of robotics in real-world city environments

# Requirements

# How to use

To set up and run RoboCat on your system, follow these simple steps:
### Step 1: Download the repository
Open your terminal and run the following command:
```bash
git clone https://github.com/joanmarc28/Robocat.git
```
### Step 2: Install dependencies
Make sure you have Python installed. You can set up the required environment using pip by running requirements.txt file:
```bash
pip install -r requeriments.txt
```
#### How do I install Python?
If you don't have Python installed, download it from the official website:
[https://www.python.org/downloads/](https://www.python.org/downloads/)
You can check your Python version by running:
```bash
python --version
```
### Step 3: Run the system
Once everything is installed, you can run the setup file:
```bash
bash setup_robocat.sh
```
Make sure the robot is powered on and properly connected before executing the .sh file.


# Components

## Hardware 

## 3D Design

All RoboCat 3D parts have been designed using Autodesk Fusion 360. The structure is divided into the following sections:

### Legs

| Full Leg |
|----------|
| [Leg IMG] <br> [Upper Leg Front (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/legs/upper_legFront.stl) <br> [Upper Leg Back (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/legs/upper_legBack.stl) <br> [Lower Leg Paw (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/legs/paw_leg.stl) |

---

### Body

| Chassis | Second Floor Plate | Front Body |
|---------|--------------------|------------|
| [Chassis IMG] <br> [Chassis (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/chassis/chassis.stl) | [2FloorPlate IMG] <br> [2nd Floor Plate (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/2nFloor_Plate/2nFloor_Plate.stl) | [FrontBody IMG] <br> [Front Body (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/front_body/front_body.stl) |

| Middle Body | Back Body | Neck |
|-------------|-----------|------|
| [MiddleBody IMG] <br> [Middle Body (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/middle_body/middle_body.stl) | [BackBody IMG] <br> [Back Body (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/back_body/back_body.stl) | [Neck IMG] <br> [Neck (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/neck/neck.stl) |

---

### Head

| Head Model | Head Back Panel |
|------------|-----------------|
| [HeadModel IMG] <br> [Head Model (View Files)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/head/head.stl) | [Head Back Panel] <br> [Head Back Panel (View Files)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/head/head_back_panel.stl)

---

### Miscellaneous

| Tail | Fan Blades | Fan Holder |
|------|------------|------------|
| [Tail IMG] <br> [Tail (View Files)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/tail/tail.stl) | [FanBlades IMG] <br> [Fan Blades (View File)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/fan/fan_blades.stl) | [FanHolder IMG] <br> [Fan Holder (View Files)](https://github.com/joanmarc28/Robocat/blob/main/3D_files/fan/fan_holder.stl) |

---

# Software
The RoboCat software is composed of two main components:
- License Plate Detection Algorithm
- Web Application

## License Plate Detection Algorithm
RoboCat integrates a computer vision system that operates in three phases to detect and process license plates:
#### 1. Vehicle Detection
Using YOLOv8n object detection model, RoboCat identifies vehicles present in its field of vision. Specifically, the system is trained to detect only conventional passenger cars, which is the only object class configured in the YOLO model for this detection task. This selective approach ensures optimized performance and reduces false positives from unrelated objects.

#### 2. License Plate Detection
Once a vehicle is detected, a second YOLOv8n model is used to accurately locate the license plate area. The system also detects and extracts the nationality region by identifying the blue section commonly present on Spanish license plates. Since our project only focuses on Spanish license plates, the blue section is cropped for further processing.

#### 3. Optical Character Recognition (OCR)
A custom CNN (Convolutional Neural Network) using Tensorflow is applied to convert the plate characters into text. The algorithm validated the result to ensure it follows the standard Spanish license plate format (1234 BCD). Additional correction steps are included to handle character misinterpretations and adapt the output to the expected structure.

## Web Application

The RoboCat web application includes two user profiles.

### Police Officer
Authorized officers can access a control interface to monitor and manage RoboCat units in real-time:
- Live location tracking (GPS coordinates)
- Internal system monitoring, including controllers temperature
- Real-time video feed from RoboCat's onboard camera
- Remote control commands such as "Crouch" or "Stand Up"

In addition, officers can manage regulated parking areas through the Parking Zone Management page, where new parking zones can be defined by specifying latitude and longitude boundaries.
Officers also have access to the Infraction Database, where they can review all detected violations, manually validate or dismiss possible infractions, and issue fines when necessary.

### Client (Vehicle Owner)

Registered users can manage their vehicles and parking sessions through the web platform:
- Register one or more vehicles by providing license plate, brand, model and official DGT data.
- Pay for parking in regulated zones by selecting a registered vehicle and specifying the desired parking duration
- Active parking sessions are displayed on the main dashboard with a countdown timer showing the remaining time.

If a vehicle is parked without a valid registration in a regulated area and RoboCat scans its license plate, and infraction is automatically recorded. The system notifies the vehicle owner of the violation and provides the fine details.

# Tech Stack
### Programming & AI
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Ultralytics](https://img.shields.io/badge/ultralytics-a061ff.svg?style=for-the-badge&logo=YOLO&logoColor=ffffff&labelColor=a061ff)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
  
### 3D Design & Hardware
![AutoDeskFusion](https://img.shields.io/badge/autodesk fusion-ff944d.svg?style=for-the-badge&logo=Autodesk&logoColor=ffffff&labelColor=ff944d)
![Fritzing](![badge](https://img.shields.io/badge/fritzing-d63222.svg?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAIAAACRXR/mAAAAxHpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBbDgMhCPz3FD2CPHThOO6jSW/Q4xeU3axtJ2FEhoxIOt6vZ3o4EDhxWaRqrdnAyorNEskDrTNk7txBGBrM9XQJaCXyznGVGv1nHS6DcTTLys1IthDWWVAOf/kyiofJJ/J8DyPdrpG7AGHQxrdyVVnuX1iPPENGJCeWeeyf+2Lb24u9Q4gHAWVjIh4DkEdJ1CypxkhsjWANXinGhTTMbCH/9nQifQDi3lkaxxbeIwAAAYRpQ0NQSUNDIHByb2ZpbGUAAHicfZE9SMNQFIVPU7WiFQc7FHHIUJ3soiKOpYpFsFDaCq06mLz0D5o0JCkujoJrwcGfxaqDi7OuDq6CIPgD4i44KbpIifclhRYxPni8j/PeOdx7HyA0q0w1e2KAqllGOhEXc/lVMfCKPoQxCCAiMVNPZhaz8Fxf9/Dx8y7Ks7zf/bmGlILJAJ9IHGO6YRFvEM9uWjrnfeIQK0sK8TnxpEEFEj9yXXb5jXPJYYFnhoxsep44RCyWuljuYlY2VOIZ3qOiapQv5FxWOG9xVqt11q6TdxgsaCsZrtMeQwJLSCIFETLqqKAKC1E6NVJMpOk+7uEfdfwpcsnkqoCRYwE1qJAcP/gf/J6tWZyecpOCcaD3xbY/xoHALtBq2Pb3sW23TgD/M3Cldfy1JjD3SXqjo0WOgOFt4OK6o8l7wOUOEH7SJUNyJD9toVgE3s/om/LAyC0wsObOrX2P0wcgS7NavgEODoGJEmWve/Td3z23f9+05/cDgMhyrGRB+HoAAA12aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOjQ5M2JkOTY5LWE5YzYtNGRjZC05YWJhLWEwNjlhYzVmNDc5YyIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo4MWRlMTNiYi03ZjQzLTQwMDMtYTJjNy03OTA3NTUzOTNmNDIiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDozNjdlMTZjYS1hZTM1LTRiOTYtYTYxMS1mNGViY2I3YzA3NDAiCiAgIEdJTVA6QVBJPSIyLjAiCiAgIEdJTVA6UGxhdGZvcm09IldpbmRvd3MiCiAgIEdJTVA6VGltZVN0YW1wPSIxNzUwNzYzMTYxMDAwOTk1IgogICBHSU1QOlZlcnNpb249IjIuMTAuMzQiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCIKICAgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyNTowNjoyNFQxMzowNTo1OSswMjowMCIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjU6MDY6MjRUMTM6MDU6NTkrMDI6MDAiPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDphNTljYjEzYy1kNDg0LTQzMWItOWExMi1hYmM5NDk5OWVhYmUiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjUtMDYtMjRUMTM6MDY6MDEiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+MkMs0AAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+kGGAsGAL19Il0AAAMySURBVFjDY7xmpMQw+AATw6AEo84aBs5ioapp/1m0jNnUtZm4uNEk/rx68WPfFoa/f+jrLEYmwZJGIRc3NhERXEp+val80tnyc99mOkUio6CY7OKNEhFReNzEwMDAJiIilpxOp9BiZOeUnb6QW1WNGMWsQkJ0SvIidV1EuomBgeHPhw/0cBaTmKyQozORin9//PhqwRx6RCJ3QBgTOzuyyL+fP98d2Pf7w4f/Xz4z/P8PzZ8MDH+eP/u+a+P/b5/p4SxOFVU0kRfLl3yc3DbAxSmLkDBqsfX/87J5A1/KM7GxocTgjx//3jwfDJUPI1opjy5A18rn/3+Gf79hqRnFVQx/fsNcxsjAzEq+d0lqBrKaOojnFHDKy7Pw8hFw+d+/vz+8/3z+/Oum8v9fP9LSWf//K249wiEpRZIFr7dve1OTS8O0xSytSKqbGBgYuDU1aZvk/3359P/vX1It+PfjB22d9f/Tu4/nzpCWN/79e79nF82TPAMzM19KIbeeARMnJwMDA6eCIis/P1Iy//P5yhU47/fbt5927/ixaz3tnYUKZBZt4tXWRsTX9283bXQYqFF2jXYxRp016qxRZ40oZzGysqL1rRkFxAfSWUwyKrJLt/CoofQQmTg4lFZt4XANpNxZzNmSgqT3pLnk5izlxuj2MDAwMHNx8VlZf7528+/T+/QOLaGyRi4FRZwe5eKWKCihe1v+/39BO3s4782rV5tWLPv86ZO7f4CGrh606aemzmbp/Ov4Xvo5i0XbhBXWPfz3719HSeGNLcsYGBj2Te+dc/amqIQERIrL0pYSZ5EcicxIXdavnz9B3MTAwPD3+6dnT58gzOXhoWva+vMC0UHl4eM3js6EdvwllOQUFOBSfz9+pGva+nv70s9XL9nFxBkYGBgZGUta2vdYWn/59NHe3UNQWASe/r4d2kvfJM/I+H7vHonIaAiPl58/MCoaTcnnK5d/nz9G7wLifV/Dl+vXcMn+/vjxRVfLQJTy//49yYr/cOokfAQLDn48efywrODPtbMUOouiLgaHZwi/uxe7hCQjM/Pv9+8/nzz+ecFUhr+/Ka98GEenokadNbKcBQBm2BbRXQTF+wAAAABJRU5ErkJggg==&logoColor=ffffff&labelColor=d63222))
![EasyEda](![badge](https://img.shields.io/badge/easyeda-5d8dff.svg?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAIAAAC0Ujn1AAAAxXpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVDbDcMwCPxnio5gA36N4zSp1A06fs8GR01UJB+PQ2eAjs/7RY9hHJU0lZpbzgGmTRt3BDWY9Ykx6ERLDufitU4nwSgJvFhas/evejwFzHVE6UeoPp3YrkRT1683If9IxkSMYHeh5kLCRkQX6LZWyK2W3xW2tcGyao8GSJnap8g914Lr7QlFYT4kSgCKqA0g4yWSjiADWRSNEQ19Uh1R80lwkH93WkZfdVNZgGYZqTkAAAGEaUNDUElDQyBwcm9maWxlAAB4nH2RPUjDUBSFT1O1ohUHOxRxyFCd7KIijqWKRbBQ2gqtOpi89A+aNCQpLo6Ca8HBn8Wqg4uzrg6ugiD4A+IuOCm6SIn3JYUWMT54vI/z3jncex8gNKtMNXtigKpZRjoRF3P5VTHwij6EMQggIjFTT2YWs/BcX/fw8fMuyrO83/25hpSCyQCfSBxjumERbxDPblo6533iECtLCvE58aRBBRI/cl12+Y1zyWGBZ4aMbHqeOEQslrpY7mJWNlTiGd6jomqUL+RcVjhvcVarddauk3cYLGgrGa7THkMCS0giBREy6qigCgtROjVSTKTpPu7hH3X8KXLJ5KqAkWMBNaiQHD/4H/yerVmcnnKTgnGg98W2P8aBwC7Qatj297Ftt04A/zNwpXX8tSYw90l6o6NFjoDhbeDiuqPJe8DlDhB+0iVDciQ/baFYBN7P6JvywMgtMLDmzq19j9MHIEuzWr4BDg6BiRJlr3v03d89t3/ftOf3A4DIcqxkQfh6AAANdmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDphN2M2YWMxNC1iMjVlLTQ4YzMtOGM4NC1kZDFjNDFmNjRhZTYiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MTFmM2Q5MzItZjA5OC00NjdkLWE3YjctMTUzODg4MzliMzc4IgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ODdhYWMyNWQtMDFlNS00YmJjLTg0ZGEtZGJiYjdlYjAyYTY0IgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTc1MDc2Mjk2MTUwNTE5OSIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjM0IgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjU6MDY6MjRUMTM6MDI6MzkrMDI6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDI1OjA2OjI0VDEzOjAyOjM5KzAyOjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6M2M5M2YwZmMtMmU5MS00YTBkLTgxOWMtN2JiNjhmY2Y3ZmU2IgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKFdpbmRvd3MpIgogICAgICBzdEV2dDp3aGVuPSIyMDI1LTA2LTI0VDEzOjAyOjQxIi8+CiAgICA8L3JkZjpTZXE+CiAgIDwveG1wTU06SGlzdG9yeT4KICA8L3JkZjpEZXNjcmlwdGlvbj4KIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAKPD94cGFja2V0IGVuZD0idyI/PseLl1AAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfpBhgLAimbo381AAAC0ElEQVRIx+2WyU9TURSHv/eAgtSCCC1DRaAEJKIICogKRNGoIDjgFGNg4cKFGhON/wEbE4edGxIXJoaFEWKUsGCIApYAQWSoFUjQoFIZChhoHyBtnwuqDdIymOCK3/Lcc7/8cs+5516h6IHM2khkzbSO/n9o75Uk+ftwNImESAJVIDMxxccBqg3M2pbaJSzbfLlJnDyAcsPf8SkrFY3UGf/VdXEmh9MRALBOMzwOEBaMvx8qJcXHCFbxrGXF6D1bydpBeAiiiCYIAaQZXump6kKWAbxEClLI24efgrz9fDPT1L8cWuHFjVx2xTttzmtmlofP6RtxRewOXrzj0xA3C1H4UJjtHr2gQ24VkByPAHY7X4b4NIg0Q23bAu4fdQ3S0AGgCeJuEWnRnl0f2U6iDsA0yqNKvk4A+HkjCB4rUdVOTiqiQISaa6cpq6bG6M515k6A6VnuVzi5wIyN6TmPaLOV0pe87cRmx0vkfA6aje7QEWqA3gHM1uU7PUlLgC9AUz+ldZTVAPgpOJ6yCC0KKHwALNIy0AwdJZe4c5GzGa5grZHxSYCosEVn7ZCxSAQoCd3sXAj2pyCV8BCmJOq76DaxN4YTGUSHOxMSY6DeBbLZALxFd2X8bGJXHLGRpEVjnuLOOVRK51JqAt/NaDW/C/CT1g+UN7so8RpCNgEMT7hDV7aQqMPbi6v5TFpRKTGNojcQG8HubU7u7E9ajZQ3My4BCAKiQIaOC4cQRWSZBoM7dO8IlXpOZeGrQK3A7uBeOWMSvKckkKgwDP08rmHsdzGuHCQ7BQFXdzZ1YzB5uI0VbUxKnM4iQIksM21bcI6Gzy7uH8vzmrPR2MmT+iVnSK2RNz2UXEar5vZJ6tqJ06LTYnfQMbAg0zCA3QEyPyzo+xi1rGyoJm/h+hl8fVyR6hae6lf3FHic13Fq8tMJDcYioTfwumfVr4yw/g9ZRy+pX7ga8DYsF6EsAAAAAElFTkSuQmCC&logoColor=ffffff&labelColor=5d8dff))

### Simulation & Development Tools
![badge](https://img.shields.io/badge/coppelia robotics-d63222.svg?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAIAAACRXR/mAAAAw3pUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVBbDgMhCPznFD2CPHTxOO6jSW/Q4xeU3axtJxGRmYwAHO/XEx4OQgHJi5ZaSjJIlUrNEk0DrUdM0mMHU3A41+EiyErsyvHUEvqzjpfBuJpl+WakWxDrTFQJf/0yio/ZO/J8D6O6XS13AsOgjbFSqbrcR1iPNEPHAQ+ic9s/78W2t2f7h4kORk4WmWU0wH4ycLOkWCQWE6IJmkt7/RzVFvJvTyfgA+C2WQ3qsx0gAAABhGlDQ1BJQ0MgcHJvZmlsZQAAeJx9kT1Iw1AUhU9TtaIVBzsUcchQneyiIo6likWwUNoKrTqYvPQPmjQkKS6OgmvBwZ/FqoOLs64OroIg+APiLjgpukiJ9yWFFjE+eLyP89453HsfIDSrTDV7YoCqWUY6ERdz+VUx8Io+hDEIICIxU09mFrPwXF/38PHzLsqzvN/9uYaUgskAn0gcY7phEW8Qz25aOud94hArSwrxOfGkQQUSP3JddvmNc8lhgWeGjGx6njhELJa6WO5iVjZU4hneo6JqlC/kXFY4b3FWq3XWrpN3GCxoKxmu0x5DAktIIgURMuqooAoLUTo1Ukyk6T7u4R91/ClyyeSqgJFjATWokBw/+B/8nq1ZnJ5yk4JxoPfFtj/GgcAu0GrY9vexbbdOAP8zcKV1/LUmMPdJeqOjRY6A4W3g4rqjyXvA5Q4QftIlQ3IkP22hWATez+ib8sDILTCw5s6tfY/TByBLs1q+AQ4OgYkSZa979N3fPbd/37Tn9wOAyHKsZEH4egAADXZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+Cjx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDQuNC4wLUV4aXYyIj4KIDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+CiAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgIHhtbG5zOkdJTVA9Imh0dHA6Ly93d3cuZ2ltcC5vcmcveG1wLyIKICAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICB4bXBNTTpEb2N1bWVudElEPSJnaW1wOmRvY2lkOmdpbXA6NjQzNzcwYTgtZTU3ZC00NzZjLTlmYjgtOWI0NGQ5ZjJkZDdlIgogICB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjNkZmQyOTBhLTk0YmQtNDJkYi1iZTczLTE3MzZiOGRiYTE1NiIKICAgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOmMwMzBiZjQ3LTc4YWEtNDQ4YS05ZTZiLTc0YjQzMzllYWNlZCIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iV2luZG93cyIKICAgR0lNUDpUaW1lU3RhbXA9IjE3NTA3NjM0MDcwOTkyMDkiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zNCIKICAgZGM6Rm9ybWF0PSJpbWFnZS9wbmciCiAgIHRpZmY6T3JpZW50YXRpb249IjEiCiAgIHhtcDpDcmVhdG9yVG9vbD0iR0lNUCAyLjEwIgogICB4bXA6TWV0YWRhdGFEYXRlPSIyMDI1OjA2OjI0VDEzOjEwOjA1KzAyOjAwIgogICB4bXA6TW9kaWZ5RGF0ZT0iMjAyNTowNjoyNFQxMzoxMDowNSswMjowMCI+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjlhYjRiZmJjLTFiYTYtNGFlYS1iMGUzLTIxYWEzZTQ3NjMzZiIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChXaW5kb3dzKSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyNS0wNi0yNFQxMzoxMDowNyIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz4RE2+RAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH6QYYCwoHj6z48gAABKdJREFUWMPtmX9MG2UYx5/3rtdre4WCUMbqYRfWZCYL0w0z4xIlOs2miUED/haXOTWOjQSnQdBo9gfMhWwk+oeLxJhF3RKNbjISXRY3FSELOlE2XDaw4zdoC1doae96P97XP8paIPzsjnkxvH/dm/d697n3+T7P+33fosubcsF4jQJDthWsFaz/ERaypTp2V6ZXvQeEGAWL4j38J184i4qly38Czcx1m2lZXq6pgFUwmQFN+2zKlZvzQb02MeEtfoQE/p4xuoxYyOFMK91nz9tgzsgca/pp9EAlEDw5xNr4ug8tLld3+R4y5puHSW8sxpJz5Ci37vZYz1n4mOL3BesPAQAQnLn/EOfx+BpOyq3nbqrkEU0DRU/tZj9XglIyASBl176MrQ+Kvb3C4ep5lD47FnXrWlvxTmAsyWERKTzwxt5IT09CY7IMBNtLSl27XiayPFxXSyLjSy4Q9qKn3ZVvZ9fVI86RHBke+Kt/70vS4CAAEFX1ffVlVvVhvqwcMYzv5Iloy+lFPofeszo98VBiSi14gPN4zBs3h9vaSFCYI9EUAAQ0A4gCVQYg0/RLmbit21hnFqKo1Py7rG43AIx8961w4E0AtFg9zDA2TP59rqp3bWvWyILwz+efRjva1UsXiDgONAMIAQCTX5BRspN1u00cB4RgRVGGh8W+PtXvw2LYzLsdW7aw2dmJT5Ak/6lvAger5k+9BbAAAJmtKTtKHQX3W3meYllNkrRQKNzVGfzhrNh4nF53Jx7qp1y3sXdstG++x56Xx2Y6Y8SzyY0MfPxR6EjtnDcsHut6RDXKlZvyxPPOwseZ9HQAIBiHLl4crijDo0Px1yJbmvnuAsdD2y2etQRjIisp69cnqDDurd4vNhxbclIv6E5Rxuq0V8sztz1s4jgAkH2+YNtvUudV5ZpX9l4lAT8RgzEGAEivqMl+6plEBEXR+2ShNuTVH2tSc5vuzSp7LTVvQyIchBCMVUGI9HSHfmmNnDuN7A6+ptbK8/FfBdv/GHyxKJkSuAQvjyju2VdWlexgnVmzqEhRACFkMk2NYN/BmsjXR5PAmlYgFqyXyqULY42nVBPL8jm01TqjxCNqWq4FWprH3q+Jr4nLhwUAANGIdP7H8eYWjbGwLhdlmX1JiHRfG37rdRISkivLS8eKzduYX2w6M/5zi2a2MLdk0Bw3dTTY0TH0TgXu70x+eb3xfSKVtsrT+D1ts8W6E1euDOx+gQRH/2PTjEcHSNwUEDJy/LMbZNLL2CAcDieqhiwbY4uBEFGUSSpNwwHBGFiAcDQ6GVBVVXu9BsHCFMvGSyj2Dxpmn0hPemVVEAArRsEiWItdyCN+oChjYBFAjDl2KXZ1Ld6CLncmQiwTiaZFfm01zBkEojRRjGFFm88Y52gEkagEAGowSFTZOLOF1IkJAJBHRgBj48wWRHu6AQArSsw6GwZraDBu5w2EJbU0YUXRpTToWuVjFl43Kp2w7NsfpRiGomm90HTSVvvvRNNMjjRdVh79tHX+LNG0+IJtGG1pKtE0NRBIbvs1i1b1wcJauLNTaDixmJO+m7TzuX4cYAFFMlgQAXRkgpU/V5bW/gWG1/PrMhi6ygAAAABJRU5ErkJggg==&logoColor=ffffff&labelColor=d63222)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) (Development environment)
![badge](https://img.shields.io/badge/python dotenv-3776ab.svg?style=for-the-badge&logo=Python&logoColor=ffffff&labelColor=3776ab)

### Web Application
- **Backend:** ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) (High-perfomance Python web framework)
- **Frontend:** ![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black) (Dynamic HTML rendering)
- **Database:** ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) (With SQLAlchemy ORM)
- **APIs & External services**:
  - ![badge](https://img.shields.io/badge/google cloud vision-4285f4.svg?style=for-the-badge&logo=Google Cloud&logoColor=ffffff&labelColor=4285f4)
  - ![badge](https://img.shields.io/badge/google cloud speech-4285f4.svg?style=for-the-badge&logo=Google Cloud&logoColor=ffffff&labelColor=4285f4)
  - ![Google Gemini](https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white) (AI integration)
  - ![badge](https://img.shields.io/badge/AIORTC-2c5bb4.svg?style=for-the-badge&logo=AIOHTTP&logoColor=ffffff&labelColor=2c5bb4)
  
# License
This project is licensed under the [MIT License](LICENSE).  
© 2025–present [Contributors](https://github.com/joanmarc28/Robocat/contributors)

# Contribution
This project was created as part of a university assignment and is not open to external contributions.

However, feel free to fork the repository and experiment with it for learning and improvement purposes.

# Credits

# Gallery
