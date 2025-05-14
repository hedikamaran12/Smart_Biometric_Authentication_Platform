# Import necessary libraries
import cv2  # OpenCV library for video capturing and drawing on frames
import os  # For accessing the file system (folders, files)
import numpy as np   # NumPy for numerical operations, used here for array handling
import face_recognition  # Face Recognition library for detecting and encoding faces
from datetime import datetime  # For getting the current date and time
from tkinter import messagebox, simpledialog  # For displaying GUI message boxes to the user

# Define a class to handle core face recognition functionalities
class FaceRecognitionCore:
    def __init__(self, dataset_dir='dataset'):
        """
        Initialize the FaceRecognitionCore class.

        Parameters:
        dataset_dir (str): Directory where the known faces (dataset) are stored.
        """
        self.dataset_dir = dataset_dir  # Directory path containing face images
        self.known_face_encodings = []  # List to store face encodings
        self.known_face_names = []  # List to store names corresponding to encodings
        self.attendance_today = set()  # Set to keep track of who has been marked present today
        self.load_known_faces()  # Load faces immediately upon initialization

    def load_known_faces(self):
        """
        Load all known faces from the dataset directory and compute their encodings.
        """
        for person_name in os.listdir(self.dataset_dir):
            person_path = os.path.join(self.dataset_dir, person_name)
            if not os.path.isdir(person_path):
                continue  # Skip if it's not a folder

            # Iterate through each image in the person's folder
            for img_name in os.listdir(person_path):
                img_path = os.path.join(person_path, img_name)
                image = face_recognition.load_image_file(img_path)  # Load image file
                encodings = face_recognition.face_encodings(image)  # Extract face encoding

                if encodings:
                    # If at least one face encoding is found, store the first one
                    self.known_face_encodings.append(encodings[0])
                    self.known_face_names.append(person_name)

    def mark_attendance(self, name):
        """
        Mark the attendance of the recognized person into a CSV file.

        Parameters:
        name (str): The name of the recognized person.
        """
        if name in self.attendance_today:
            return  # Avoid duplicate attendance for the same person

        self.attendance_today.add(name)  # Add to today's attendance list
        time_now = datetime.now().strftime('%H:%M:%S')  # Current time
        date_now = datetime.now().strftime('%Y-%m-%d')  # Current date

        # Append the attendance record to a CSV file
        with open('attendance.csv', 'a') as f:
            f.write(f'{name},{time_now},{date_now}\n')

    def run_attendance(self, camera_index=0):
        """
        Run the face recognition process to mark attendance live using webcam.

        Parameters:
        camera_index (int): The index of the camera to use. Default is 0.
        """
        cap = cv2.VideoCapture(camera_index)  # Use the selected camera index
        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Unable to access the camera.")
            return

        while True:
            ret, frame = cap.read()  # Capture frame-by-frame
            if not ret:
                break  # If capturing fails, exit the loop

            # Resize the frame for faster face recognition processing
            small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

            # Find all faces and their encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_small)
            face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

            # Compare each detected face with known faces
            for encoding, loc in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(self.known_face_encodings, encoding, tolerance=0.5)
                face_distances = face_recognition.face_distance(self.known_face_encodings, encoding)

                # Scale back face locations to original size
                top, right, bottom, left = [v * 4 for v in loc]

                if face_distances.size > 0 and matches[np.argmin(face_distances)]:
                    # If a known face is recognized
                    name = self.known_face_names[np.argmin(face_distances)]
                    self.mark_attendance(name)  # Mark the attendance
                    color = (0, 255, 0)  # Green for recognized faces
                else:
                    # If face is not recognized
                    name = "UNKNOWN"
                    color = (0, 0, 255)  # Red for unknown faces

                # Draw a rectangle around the face and label it
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            # Display the resulting frame
            cv2.imshow("Face Recognition Attendance - Press 'Q' to Quit", frame)

            # Break loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Attendance Finished", "Face recognition attendance session has ended.")
