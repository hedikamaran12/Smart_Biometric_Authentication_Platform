# -------------------------------------------------------
# Import Required Libraries
# -------------------------------------------------------

import tkinter as tk  # Tkinter library for building the graphical user interface (GUI)
from tkinter import messagebox, ttk, Toplevel, Label, PhotoImage  # Specific Tkinter widgets and components
from face_core import FaceRecognitionCore  # Custom module handling face recognition logic
from face_register import FaceRegister  # Custom module for registering new faces
import threading  # For running tasks in parallel threads
import time  # For time-related operations (delays, timeout)
import csv  # For reading and writing CSV files
import os  # For operating system-level operations (path handling, file reading)
import cv2  # OpenCV library for accessing camera and image processing
import face_recognition  # Face recognition library built on dlib
from PIL import Image, ImageTk  # Python Imaging Library for image manipulation and display in Tkinter
from datetime import datetime  # For fetching and formatting current date and time

# -------------------------------------------------------
# SplashScreen Class
# Displays a loading screen before the main application
# -------------------------------------------------------

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        """
        Initialize the Splash Screen Window.

        Parameters:
        parent (tk.Tk): The parent window object.
        """
        super().__init__(parent)
        self.configure(bg="#1e2a38")
        self.overrideredirect(True)  # Remove window decorations (title bar, etc.)

        # Set splash screen to full screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Load and display the application logo
        logo_image = Image.open("logo.png")
        self.logo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(self, image=self.logo, bg="#1e2a38")
        logo_label.place(relx=0.5, rely=0.4, anchor="center")

        # Display loading text
        loading_text = tk.Label(
            self,
            text="Loading Secure Biometric System...",
            font=("Helvetica", 16, "bold"),
            bg="#1e2a38",
            fg="white"
        )
        loading_text.place(relx=0.5, rely=0.65, anchor="center")

        # Automatically destroy splash screen after 3 seconds
        self.after(3000, self.destroy)
# -------------------------------------------------------
# FaceRecognitionApp Class
# Main Application Window for Biometric Authentication System
# -------------------------------------------------------

class FaceRecognitionApp:
    def __init__(self, master):
        """
        Initialize the main Face Recognition Application.

        Parameters:
        master (tk.Tk): The root window of the application.
        """
        self.master = master
        master.title("Biometric Authentication System")
        master.geometry("800x600")
        master.configure(bg="#1e2a38")
        master.minsize(600, 400)

        # Instantiate the Face Recognition Core and Face Registration Modules
        self.attendance = FaceRecognitionCore()
        self.registrar = FaceRegister()

        # Detect available camera index
        self.camera_index = self.detect_camera_index()

        # Configure custom style for GUI buttons
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Rounded.TButton",
                        font=("Helvetica", 14, "bold"),
                        padding=10,
                        background="#3498db",
                        foreground="white",
                        relief="flat",
                        borderwidth=0)
        style.map("Rounded.TButton",
                  background=[('active', '#2980b9')],
                  foreground=[('active', 'white')])

        # Load and display the application logo
        try:
            self.logo = PhotoImage(file="logo.png")
            logo_label = tk.Label(master, image=self.logo, bg="#1e2a38")
            logo_label.pack(pady=(30, 10))
        except Exception:
            pass  # If logo not found, continue without crashing

        # Application Title
        self.title_label = tk.Label(
            master,
            text="Biometric Authentication System",
            font=("Helvetica", 22, "bold"),
            bg="#1e2a38",
            fg="#ecf0f1"
        )
        self.title_label.pack(pady=10)

        # Sub-title
        self.sub_label = tk.Label(
            master,
            text="Choose a biometric authentication method",
            font=("Helvetica", 14),
            bg="#1e2a38",
            fg="#bdc3c7"
        )
        self.sub_label.pack(pady=10)

        # Frame to hold the main buttons
        self.button_frame = tk.Frame(master, bg="#1e2a38")
        self.button_frame.pack(pady=30)

        # Fingerprint Authentication Button (future implementation)
        self.fingerprint_button = ttk.Button(
            self.button_frame,
            text="Fingerprint Authentication",
            command=self.open_fingerprint_window,
            style="Rounded.TButton"
        )
        self.fingerprint_button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Face Recognition System Button
        self.face_button = ttk.Button(
            self.button_frame,
            text="Face Recognition System",
            command=self.open_face_system,
            style="Rounded.TButton"
        )
        self.face_button.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        # Admin Mode Button
        self.admin_button = ttk.Button(
            master,
            text="Admin Mode",
            command=self.open_admin_mode,
            style="Rounded.TButton"
        )
        self.admin_button.pack(pady=10)

        # Configure the button frame columns for proper stretching
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        # Footer Section with Credits
        self.footer = tk.Label(
            master,
            text="Prepared By: Hedi Kamaran \n© 2025 Erbil Polytechnic University",
            font=("Helvetica", 10),
            bg="#1e2a38",
            fg="#95a5a6"
        )
        self.footer.pack(side=tk.BOTTOM, pady=10)
    def detect_camera_index(self):
        """
        Detect the available camera index.

        Returns:
        int: The index of the available camera device.
        """
        try:
            cap = cv2.VideoCapture(1)  # Attempt to open the second camera (index 1)
            if cap.isOpened():
                cap.release()
                return 1  # Camera index 1 is available
        except Exception:
            pass  # If camera index 1 not available, fall back

        return 0  # Default to primary camera (index 0)

    def open_fingerprint_window(self):
        """
        Display a placeholder window for the fingerprint authentication feature.
        """
        win = Toplevel(self.master)
        win.title("Fingerprint Authentication")
        win.geometry("400x200")
        win.configure(bg="#fefefe")
        Label(win, text="Feature Coming Soon...", font=("Helvetica", 16), bg="#fefefe", fg="#c0392b").pack(pady=60)

    def open_face_system(self):
        """
        Launch the Face Recognition attendance system.
        """
        try:
            messagebox.showinfo("Starting", "Starting Face Recognition...")
            self.attendance.run_attendance(camera_index=self.camera_index)  # <--- updated
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_admin_mode(self):
        """
        Launch the Admin Mode after verifying the user's identity via face recognition.
        """
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Unable to access the camera.")
            return

        # Dataset location where admin images are stored
        dataset_base = r"D:\\s8\\final project\\other resource\\xom\\dataset"
        admin_list = []

        # Load the list of registered admins
        if os.path.exists("admins.txt"):
            with open("admins.txt", "r") as f:
                admin_list = [line.strip() for line in f if line.strip()]

        if not admin_list:
            messagebox.showerror("Access Denied", "No admins configured.")
            return

        # Load encodings for all admin faces
        known_encodings = []
        for admin_name in admin_list:
            admin_folder = os.path.join(dataset_base, admin_name)
            if os.path.exists(admin_folder):
                for img_name in os.listdir(admin_folder):
                    img_path = os.path.join(admin_folder, img_name)
                    image = face_recognition.load_image_file(img_path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        known_encodings.append(encodings[0])

        verified = False
        timeout_seconds = 10  # Maximum time to attempt verification
        start_time = time.time()

        # Begin verification loop
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # Process the frame for face detection
            small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small)
            face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

            # Compare detected faces with known admin faces
            for encoding in face_encodings:
                matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=0.5)
                if True in matches:
                    verified = True
                    break

            # Display prompt on the verification window
            cv2.putText(frame, "Show your face for Admin Access", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.imshow("Admin Verification - Press 'Q' to cancel", frame)

            # Break conditions: face verified, timeout reached, or user pressed 'Q'
            if verified:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if time.time() - start_time > timeout_seconds:
                break

        cap.release()
        cv2.destroyAllWindows()

        if verified:
            self.launch_admin_window()
        else:
            messagebox.showerror("Access Denied", "Face not recognized as Admin.")
    def launch_admin_window(self):
        """
        Launch the Admin Control Panel window after successful verification.
        """
        self.admin_window = Toplevel(self.master)
        self.admin_window.title("Admin Panel")
        self.admin_window.geometry("600x750")
        self.admin_window.configure(bg="#ffffff")

        # Attempt to load and display the logo
        try:
            logo_img = Image.open("logo.png")
            self.admin_logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self.admin_window, image=self.admin_logo, bg="#ffffff")
            logo_label.pack(pady=(20, 10))
        except Exception as e:
            print("Logo loading error:", e)

        # Admin Panel Title
        title_label = tk.Label(
            self.admin_window,
            text="Admin Panel",
            font=("Helvetica", 18, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        title_label.pack(pady=(5, 15))

        # Frame containing the Admin Control Buttons
        button_frame = tk.Frame(self.admin_window, bg="#ffffff")
        button_frame.pack(pady=10)

        # Admin Control Buttons
        ttk.Button(button_frame, text="View Report", command=self.view_attendance_report_from_admin, style="Rounded.TButton").grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Register Face", command=self.register_person, style="Rounded.TButton").grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(button_frame, text="Add Admin", command=self.add_new_admin, style="Rounded.TButton").grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Delete Admin", command=self.delete_admin, style="Rounded.TButton").grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(button_frame, text="Fingerprint (Soon)", command=self.open_fingerprint_window, style="Rounded.TButton").grid(row=2, column=0, columnspan=2, pady=10)

        # Admin List (TreeView)
        if hasattr(self, 'admin_tree'):
            self.admin_tree.destroy()

        self.admin_tree = ttk.Treeview(self.admin_window, columns=("Name"), show='headings', height=8)
        self.admin_tree.heading("Name", text="Admin Name")
        self.admin_tree.column("Name", width=250, anchor="center")
        self.admin_tree.pack(padx=10, pady=20, fill=tk.X)

        # Populate the admin list from the existing records
        if os.path.exists("admins.txt"):
            with open("admins.txt", "r") as f:
                admins = [line.strip() for line in f if line.strip()]
                for admin in admins:
                    self.admin_tree.insert("", tk.END, values=(admin,))

    def admin_list_view(self):
        """
        Refresh and display the list of administrators in the Admin Panel.
        """
        if hasattr(self, 'admin_tree'):
            self.admin_tree.destroy()

        self.admin_tree = ttk.Treeview(self.admin_window, columns=("Name"), show='headings')
        self.admin_tree.heading("Name", text="Admin Name")
        self.admin_tree.column("Name", width=400)
        self.admin_tree.pack(padx=10, pady=20, fill=tk.BOTH, expand=True)

        # Populate the TreeView with admin names
        if os.path.exists("admins.txt"):
            with open("admins.txt", "r") as f:
                admins = [line.strip() for line in f if line.strip()]
                for admin in admins:
                    self.admin_tree.insert("", tk.END, values=(admin,))

    def add_new_admin(self):
        """
        Promote a registered person to Admin role.
        """
        dataset_path = r"D:\\s8\\final project\\other resource\\xom\\dataset"
        persons = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]

        if not persons:
            messagebox.showerror("Error", "No persons found in dataset.")
            return

        if os.path.exists("admins.txt"):
            with open("admins.txt", "r") as f:
                current_admins = [line.strip() for line in f if line.strip()]
            available_persons = [p for p in persons if p not in current_admins]
        else:
            available_persons = persons

        if not available_persons:
            messagebox.showinfo("Info", "All persons are already admins.")
            return

        # Window to select a person to promote
        admin_window = Toplevel(self.master)
        admin_window.title("Add New Admin")
        admin_window.geometry("400x300")
        admin_window.configure(bg="#f0f4f7")

        label = tk.Label(admin_window, text="Select a person to promote as Admin:", font=("Helvetica", 12), bg="#f0f4f7")
        label.pack(pady=10)

        selected_admin = tk.StringVar(admin_window)
        selected_admin.set(available_persons[0])

        dropdown = ttk.Combobox(admin_window, textvariable=selected_admin, values=available_persons, state="readonly")
        dropdown.pack(pady=10)

        # Confirm the selected admin
        def confirm_selection():
            admin_name = selected_admin.get()
            with open("admins.txt", "a") as f:
                f.write(admin_name + "\n")
            messagebox.showinfo("Success", f"{admin_name} added as Admin!")
            admin_window.destroy()
            self.admin_list_view()

        confirm_button = ttk.Button(admin_window, text="Confirm", command=confirm_selection, style="Rounded.TButton")
        confirm_button.pack(pady=20)

    def delete_admin(self):
        """
        Remove an existing Admin from the system.
        """
        selected_item = self.admin_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No admin selected.")
            return

        admin_name = self.admin_tree.item(selected_item, "values")[0]

        if messagebox.askyesno("Confirm Delete", f"Delete {admin_name}?"):
            if os.path.exists("admins.txt"):
                with open("admins.txt", "r") as f:
                    lines = f.readlines()
                with open("admins.txt", "w") as f:
                    for line in lines:
                        if line.strip() != admin_name:
                            f.write(line)
            messagebox.showinfo("Deleted", f"{admin_name} deleted.")
            self.admin_list_view()

    def register_person(self):
        """
        Launch the face registration process for a new person.
        """
        try:
            messagebox.showinfo("Register Person", "Camera will open. Press 'S' to save, 'Q' to quit.")
            self.registrar.register_new_person()
            messagebox.showinfo("Success", "Person registered successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def view_attendance_report_from_admin(self):
        """
        Display the attendance records in a separate report window.
        """
        report_window = Toplevel(self.master)
        report_window.title("Attendance Report")
        report_window.geometry("600x500")
        report_window.configure(bg="#ffffff")

        if not os.path.exists("attendance.csv"):
            tk.Label(report_window, text="No attendance records found.", font=("Helvetica", 12), bg="#ffffff").pack(pady=20)
            return

        # Create TreeView for displaying the records
        tree = ttk.Treeview(report_window, columns=("Name", "Time", "Date"), show='headings')
        tree.heading("Name", text="Name")
        tree.heading("Time", text="Time")
        tree.heading("Date", text="Date")
        tree.column("Name", width=180)
        tree.column("Time", width=120)
        tree.column("Date", width=200)
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Populate attendance records
        with open("attendance.csv", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    tree.insert("", tk.END, values=row)

        # Display logo at the bottom if available
        try:
            logo_img = Image.open("logo.png")
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(report_window, image=logo_photo, bg="#ffffff")
            logo_label.image = logo_photo
            logo_label.pack(side=tk.BOTTOM, pady=10)
        except Exception:
            pass
def main():
    """
    Entry point of the application.
    Displays the splash screen first, then launches the main Face Recognition App.
    """
    # Initialize the splash screen window
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)  # Remove window decorations for splash
    splash_root.configure(bg="#1e2a38")

    # Set splash screen to full screen
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    splash_root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Attempt to load and display the splash logo
    try:
        logo_photo = ImageTk.PhotoImage(Image.open("logo.png"))
        logo_label = tk.Label(splash_root, image=logo_photo, bg="#1e2a38")
        logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        logo_label.place(relx=0.5, rely=0.4, anchor="center")

        # Loading text
        loading_text = tk.Label(
            splash_root,
            text="Loading Secure Biometric System...",
            font=("Helvetica", 16, "bold"),
            bg="#1e2a38",
            fg="white"
        )
        loading_text.place(relx=0.5, rely=0.65, anchor="center")

    except Exception as e:
        print("Splash screen error:", e)

    # Define a function to launch the main application window
    def launch_main():
        splash_root.destroy()  # Close the splash screen
        main_root = tk.Tk()  # Create main application window
        app = FaceRecognitionApp(main_root)  # Initialize FaceRecognitionApp
        main_root.mainloop()  # Start the main event loop

    # Schedule the main application to launch after 3 seconds
    splash_root.after(3000, launch_main)

    # Start the splash screen event loop
    splash_root.mainloop()

# -------------------------------------------------------
# Main Program Execution
# -------------------------------------------------------

if __name__ == "__main__":
    main()
