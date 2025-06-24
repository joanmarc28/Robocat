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
A custom CNN (Convolutional Neural Network) is applied to convert the plate characters into text. The algorithm validated the result to ensure it follows the standard Spanish license plate format (1234 BCD). Additional correction steps are included to handle character misinterpretations and adapt the output to the expected structure.

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
- **Python**
- **OpenCV** (Computer Vision processing)
- **Ultralytics YOLOv8n** (Vehicle and license plate detection)
- **Tensorflow/Keras** (CNN-based OCR for license plate recognition)
- **Numpy**
  
### 3D Design & Hardware
- **Autodesk Fusion 360** (3D design an prototyping of robot components)
- **Fritzing** (Hardware schematics)
- **EasyEDA** (PCB design)

### Simulation & Development Tools
- **CoppeliaSim** (Robot simulation and movement testing)
- **Visual Studio Code** (Development environment)
- **Python Dotenv** (Environment variable management)

### Web Application
- **Backend:** FastAPI (High-perfomance Python web framework)
- **Frontend:** Jinja2 Templates (Dynamic HTML rendering)
- **Server:** Uvicorn ASGI Server
- **Database:** PostgreSQL with SQLAlchemy ORM
- **APIs & External services**:
  - *Google Cloud Vision* (Image processing)
  - *Google Cloud Speech-To-text*
  - *Google Generative AI* (AI integration)
  - *AIORTC* (WebRTC real-time communication)
  - *Requests for HTTP communication*
  
# License
This project is licensed under the [MIT License](LICENSE).  
© 2025–present [Contributors](https://github.com/joanmarc28/Robocat/contributors)

# Contribution
This project was created as part of a university assignment and is not open to external contributions.

However, feel free to fork the repository and experiment with it for learning and improvement purposes.

# Credits

# Gallery
