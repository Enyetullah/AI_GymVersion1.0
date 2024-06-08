import tkinter as tk  # Import the tkinter module for GUI creation
from tkinter import filedialog  # Import filedialog for file selection dialogs
from PIL import Image, ImageTk  # Import PIL for handling images

# Import custom modules for additional functionalities (assumed to exist)
import Left_Arm_Curl_Video
import Left_Elbow_Curl_GUI
import Wide_Arm_Push_Up_Video
import Wide_Push_Up_GUI


class Upload:
    def __init__(self, weight, name):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Upload Video")  # Set the window title
        self.weight = weight  # Store the weight value
        self.name = name  # Store the exercise name

        # Disable window resizing
        self.root.resizable(False, False)

        # Set the position and size of the window
        fixedX = 500
        fixedY = 100
        self.root.geometry(f"500x500+{fixedX}+{fixedY}")

        # Load and resize the background image
        # Replace with your image path
        self.bgImage = Image.open(
            r"D:\gym\czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcm0zMDktYWV3LTAxM18xXzEuanBn.webp")
        self.bgImage = self.bgImage.resize((500, 500))
        self.bgPhoto = ImageTk.PhotoImage(self.bgImage)

        # Create a Canvas widget to hold the background image
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack(fill="both", expand=True)

        # Display the background image on the canvas
        self.canvas.create_image(0, 0, image=self.bgPhoto, anchor="nw")

        # Display the instruction text
        self.canvas.create_text(250, 50, text="Please Upload Your Workout Video:", font=("Arial", 18), fill="White")

        # Create an Upload Video button
        self.uploadButton = tk.Button(self.root, text="Upload Video",
                                      background="black", fg="white", highlightbackground="White",
                                      command=self.uploadVideo)
        self.uploadButton.place(x=200, y=100, width=100)  # Position and size of the upload button

        # Label to display the selected file path
        self.pathLabel = tk.Label(self.root, text="", background="Black", fg="White")
        self.pathLabel.place(x=30, y=200, width=450)  # Position and size of the path label

        # Create a Next button to proceed after uploading
        self.nextButton = tk.Button(self.root, text="Next", font=("Arial", 10),
                                    background="black", fg="white", highlightbackground="White",
                                    command=self.nextAction)
        self.nextButton.place(x=100, y=300, width=100, height=27.5)  # Position and size of the next button

        # Create a Back button to return to the previous screen
        self.backButton = tk.Button(self.root, text="Back", font=("Arial", 10),
                                    background="black", fg="white", highlightbackground="White", command=self.goBack)
        self.backButton.place(x=300, y=300, width=100, height=27.5)  # Position and size of the back button

        # Initialize the video path variable
        self.videoPath = None

        # Start the Tkinter main loop
        self.root.mainloop()

    # Handle the video upload process
    def uploadVideo(self):
        # Open a file dialog to select a video file
        self.videoPath = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        # Replace forward slashes with backslashes
        self.videoPath = self.videoPath.replace("/", "\\")
        self.videoPath = str(self.videoPath)
        # Update the path label to display the selected video path
        self.pathLabel.config(text=self.videoPath)

    # Handle the next button action
    def nextAction(self):
        if self.videoPath:
            self.root.destroy()  # Close the current window
            # Call the appropriate class based on the exercise name
            if self.name == "LEFT":
                # Assuming LeftCurl class is in Left_Arm_Curl_Video module
                Left_Arm_Curl_Video.LeftCurl(self.weight, self.videoPath)
            elif self.name == "WIDE":
                # Assuming WidePush class is in Wide_Arm_Push_Up_Video module
                Wide_Arm_Push_Up_Video.WidePush(self.weight, self.videoPath)
        else:
            # Show an error message if no video is uploaded
            self.pathLabel.config(text="Please upload a video first.")

    # Handle the back button action
    def goBack(self):
        self.root.destroy()  # Close the current window
        # Call the appropriate class based on the exercise name to return to the previous screen
        if self.name == "WIDE":
            Wide_Push_Up_GUI.VideoPlayer(self.weight)
        elif self.name == "LEFT":
            Left_Elbow_Curl_GUI.VideoPlayer(self.weight)


# Run the Upload class only if this script is being executed directly
if __name__ == "__main__":
    Upload()  # Replace with appropriate weight and exercise name
