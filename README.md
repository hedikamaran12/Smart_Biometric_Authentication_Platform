Biometric Authentication System
A comprehensive face recognition-based attendance system with admin controls.

Features
Face Recognition Attendance: Automatically mark attendance using facial recognition

Admin Panel: Secure admin interface with face verification

User Registration: Register new users with multiple facial poses

Attendance Reports: View and export attendance records

Data Augmentation: Advanced image augmentation for better recognition

Modern UI: Clean, professional interface with splash screen

Technologies Used
Python 3.x

OpenCV (cv2) for camera operations

face_recognition library (dlib backend)

Tkinter for GUI

PIL/Pillow for image processing

NumPy for numerical operations

Installation
Clone this repository:

bash
git clone https://github.com/yourusername/biometric-authentication-system.git
cd biometric-authentication-system
Install required dependencies:

bash
pip install -r requirements.txt
(Create a requirements.txt file with these dependencies if you haven't already:)

text
opencv-python
face-recognition
pillow
numpy
Place your dataset in the dataset directory (create one if it doesn't exist)

Usage
Run the application:

bash
python main.py
Main Interface Options:

Face Recognition System: Start attendance marking

Admin Mode: Access admin controls (requires admin face verification)

Register Face: Add new users to the system

Admin Features:

View attendance reports

Register new users

Add/remove administrators

Manage system settings

File Structure
main.py: Main application entry point

face_core.py: Core face recognition logic

face_register.py: New user registration system

dataset_augmentation_generator.py: Image augmentation for training data

attendance.csv: Attendance records storage

admins.txt: Administrator list

logo.png: Application logo (optional)

Dataset Preparation
The system expects face images to be organized in the dataset directory with subfolders for each person:

text
dataset/
├── Person1/
│   ├── 1_normal.jpg
│   ├── 2_smile.jpg
│   └── ...
└── Person2/
    ├── 1_normal.jpg
    └── ...
Use the built-in registration system to properly capture and organize new user images.

Contributing
Contributions are welcome! Please fork the repository and create a pull request with your improvements.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
All open-source libraries used in this project
Project supervisor: [Hedi Kamaran Khwrshid]
