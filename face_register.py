 # Import necessary libraries
import os  # For interacting with the operating system, like creating directories
import cv2  # OpenCV library for accessing the webcam and image processing
import tkinter as tk  # Tkinter library for GUI elements
from tkinter import simpledialog, messagebox  # Import specific Tkinter dialogs for user input and alerts

# Define a class to handle face registration
class FaceRegister:
    def __init__(self, dataset_dir='dataset'):
        """
        Initialize the FaceRegister class.

        Parameters:
        dataset_dir (str): Path where the captured images will be stored.
        """
        self.dataset_dir = dataset_dir  # Set the directory for saving the person's images

    def register_new_person(self):
        """
        Register a new person by capturing their face in different poses.
        """
        # Create a hidden Tkinter window to use GUI dialogs
        root = tk.Tk()
        root.withdraw()  # Hide the main window, only show dialogs
        name = simpledialog.askstring("Register New Person", "Enter new person's name:")  # Ask the user for the person's name
        root.destroy()  # Close the hidden window

        # If no name is entered, display a warning and stop registration
        if not name:
            messagebox.showwarning("Registration Cancelled", "No name was entered.")
            return

        # Create a directory to save images for the new person
        save_path = os.path.join(self.dataset_dir, name.strip())  # Clean name and join with dataset directory
        os.makedirs(save_path, exist_ok=True)  # Make the directory if it doesn't exist

        # Define the different poses/images we want to capture with instructions
        instructions = [
            ("1_normal.jpg", "Look straight"),  # Capture the person looking straight
            ("2_smile.jpg", "Smile"),            # Capture the person smiling
            ("3_left.jpg", "Turn left"),          # Capture the person looking to the left
            ("4_right.jpg", "Turn right"),        # Capture the person looking to the right
            ("5_maskOn.jpg", "Wear a mask"),      # Capture the person wearing a mask
        ]

        # Open the webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            # If the webcam is not accessible, show an error message
            messagebox.showerror("Camera Error", "Unable to access the camera.")
            return

        # Loop over each instruction to capture required images
        for file, msg in instructions:
            captured = False  # Flag to check if the current image is captured
            while not captured:
                ret, frame = cap.read()  # Read a frame from the webcam
                if not ret:
                    continue  # If frame reading fails, retry

                # Display the instruction on the screen
                cv2.putText(frame, msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                cv2.imshow("Registration - Press 's' to save, 'q' to quit", frame)  # Show the frame

                key = cv2.waitKey(1)  # Wait for a key press
                if key == ord('s'):
                    # If 's' is pressed, save the current frame as an image
                    cv2.imwrite(os.path.join(save_path, file), frame)
                    captured = True  # Mark as captured to move to next instruction
                elif key == ord('q'):
                    # If 'q' is pressed, cancel the registration
                    cap.release()  # Release the webcam
                    cv2.destroyAllWindows()  # Close all OpenCV windows
                    messagebox.showinfo("Registration Cancelled", "Registration was cancelled by user.")  # Inform the user
                    return

        # After capturing all images, release the camera and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        # Notify the user that registration was completed successfully
        messagebox.showinfo("Registration Complete", f"{name} has been successfully registered!")