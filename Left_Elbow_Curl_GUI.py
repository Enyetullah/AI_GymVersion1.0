import tkinter as tk  # Import the tkinter module for GUI creation
from PIL import Image, ImageTk  # Import PIL for image handling
import cv2  # Import OpenCV for video handling

# Import custom modules for additional functionalities (assumed to exist)
import Left_Arm_Curl
import Video_Upload_GUI
import Gym_GUI


class VideoPlayer:
    def __init__(self, weight):
        # Creating the main GUI window
        self.root = tk.Tk()
        self.root.title("Gumnazo")  # Set the window title
        self.weight = weight  # Store the weight value
        self.exerciseName = "LEFT"  # Set the default exercise name
        self.root.resizable(False, False)  # Disable window resizing

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

        # Display instructional text on the canvas
        self.canvas.create_text(250, 50,
                                text="For a demonstration on how to do a Wide Arm Push Up, Please watch the video \n"
                                     "below. Please Complete the exercise in a side way angle as shown:",
                                font=("Arial", 10), fill="white")

        # Set the video path and open the video file using OpenCV
        self.videoPath = r"D:\gym\Tutorial Videos\WIN_20240525_16_40_54_Pro.mp4"  # Replace with your video file path
        self.video = cv2.VideoCapture(self.videoPath)
        self.playing = False  # Initialize the playing state

        # Create a Label widget to display the video
        self.videoLabel = tk.Label(self.root, bg="black")
        self.videoLabel.place(x=80, y=80, width=350, height=350)  # Position and size of the video display

        # Create buttons for various functionalities
        self.playButton = tk.Button(self.root, text="Play Video", background="black", fg="white",
                                    highlightbackground="white", command=self.playVideo)
        self.playButton.place(x=20, y=450, width=100, height=27.5)  # Position and size of the play button

        self.realTimeButton = tk.Button(self.root, text="Real-Time Exercise", font=("Arial", 10),
                                        background="black", fg="white", highlightbackground="white",
                                        command=self.realTime)
        self.realTimeButton.place(x=130, y=450, height=27.5)  # Position and size of the real-time exercise button

        self.videoUploadButton = tk.Button(self.root, text="Video Exercise", font=("Arial", 10),
                                           background="black", fg="white", highlightbackground="white",
                                           command=self.videoUpload)
        self.videoUploadButton.place(x=265, y=450, height=27.5)  # Position and size of the video upload button

        self.backButton = tk.Button(self.root, text="Back", font=("Arial", 10),
                                    background="black", fg="white", highlightbackground="white",
                                    command=self.goBack)
        self.backButton.place(x=375, y=450, width=100, height=27.5)  # Position and size of the back button

        # Start the Tkinter main loop
        self.root.mainloop()

    # Toggle the video play and stop functionality
    def playVideo(self):
        if not self.playing:
            self.playing = True
            self.playButton.config(text="Stop Video", command=self.stopVideo)
            self.showFrame()
        else:
            self.stopVideo()

    # Stop the video playback
    def stopVideo(self):
        self.playing = False
        self.playButton.config(text="Play Video", command=self.playVideo)

    # Display video frames in the Label widget
    def showFrame(self):
        if self.playing:
            ret, frame = self.video.read()  # Read the next frame from the video
            if ret:
                # Convert the frame to RGB format and resize it
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (350, 350))
                image = Image.fromarray(frame)  # Convert the frame to a PIL image
                photo = ImageTk.PhotoImage(image)  # Convert the PIL image to a format for Tkinter
                self.videoLabel.config(image=photo)  # Update the label with the next frame
                self.videoLabel.image = photo

                self.root.after(30, self.showFrame)  # Call showFrame again after a delay for frame rate
            else:
                self.stopVideo()  # Stop the video if no more frames are available

    # Handle real-time exercise button click
    def realTime(self):
        self.root.destroy()  # Close the current window
        Left_Arm_Curl.LeftCurl(self.weight)  # Call the real-time exercise function with the weight

    # Handle video upload exercise button click
    def videoUpload(self):
        self.root.destroy()  # Close the current window
        # Call the video upload function with weight and exercise name
        Video_Upload_GUI.Upload(self.weight, self.exerciseName)

    # Handle back button click
    def goBack(self):
        self.root.destroy()  # Close the current window
        Gym_GUI.MainPage()  # Go back to the main page


# Run the VideoPlayer class only if this script is being executed directly
if __name__ == "__main__":
    VideoPlayer()  # Replace with appropriate weight value
