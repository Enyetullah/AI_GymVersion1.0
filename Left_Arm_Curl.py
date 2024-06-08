import mediapipe as mp  # Import MediaPipe for pose detection
import cv2  # Import OpenCV for video handling
import numpy as np  # Import NumPy for numerical operations
import time  # Import time for tracking the duration
import tkinter as tk  # Import tkinter for GUI operations
import Gym_GUI  # Import custom Gym_GUI module


class LeftCurl:
    def __init__(self, weight):
        # Initialize variables
        self.weight = weight  # Store the weight value
        self.counter = 0  # Initialize rep counter
        self.stage = None  # Initialize the stage (up/down) for counting reps
        self.incorrectForm = False  # Flag for incorrect form
        self.startTime = None  # Variable to store the start time

        # Initialize MediaPipe components
        self.mpDrawing = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose

        # Start the video capture and exercise tracking
        self.start()

    # Function to calculate the joint angles
    def calculateAngle(self, a, b, c):
        a = np.array(a)  # Convert point A to NumPy array
        b = np.array(b)  # Convert point B to NumPy array (vertex of the angle)
        c = np.array(c)  # Convert point C to NumPy array

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1],
                                                                    a[0] - b[0])  # Calculate the angle in radians
        angle = np.abs(radians * 180.0 / np.pi)  # Convert radians to degrees

        if angle > 180.0:
            angle = 360 - angle  # Ensure the angle is within 0-180 degrees

        return angle

    # Function to calculate calories burned
    def calorieCalc(self, weight, timeHours, count):
        if count == 0:
            return 0
        else:
            cal = weight * timeHours * 3.5  # Simple calorie calculation formula
            return cal

    def start(self):
        cap = cv2.VideoCapture(0)  # Set up video capture device (default camera)

        # Get screen width and height for centering the window
        root = tk.Tk()
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        root.destroy()  # Close the Tkinter window

        # Calculate the center position for the OpenCV window
        windowWidth = 640
        windowHeight = 480
        centerX = int((screenWidth - windowWidth) / 2)
        centerY = int((screenHeight - windowHeight) / 2)

        # Use MediaPipe Pose solution
        with self.mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            self.startTime = time.time()  # Record the start time
            while cap.isOpened():
                ret, frame = cap.read()  # Read a frame from the video capture device

                if not ret:  # Check if the video frame is not available
                    break

                # Convert the image from BGR (OpenCV format) to RGB (MediaPipe format)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False  # Disable writing to the image

                # Process the image with MediaPipe Pose
                results = pose.process(image)

                # Convert the image back to BGR for OpenCV
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark  # Get the pose landmarks

                    # Extract coordinates for shoulder, elbow, and wrist
                    shoulder = [landmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].y]

                    # Calculate the angle at the elbow
                    elbowAngle = self.calculateAngle(shoulder, elbow, wrist)

                    # Display the calculated angle on the video feed
                    cv2.putText(image, f"Elbow Angle: {elbowAngle:.2f}",
                                tuple(np.multiply(elbow, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                    # Check for proper form and count reps
                    if 35 <= elbowAngle <= 115:
                        self.incorrectForm = False  # Reset incorrect form flag

                        # Curl Counter Logic
                        if 88 <= elbowAngle <= 115 and self.stage == "up":
                            self.stage = "down"
                            self.counter += 1  # Increment the counter when moving down
                        if 88 <= elbowAngle <= 115:
                            self.stage = "down"
                        if 35 <= elbowAngle <= 50 and self.stage == "down":
                            self.stage = "up"
                    else:
                        self.incorrectForm = True  # Set incorrect form flag
                        self.stage = None  # Reset stage to ensure counter doesn't increment

                except:
                    pass  # Ignore exceptions

                # Draw the curl counter box
                cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
                cv2.putText(image, "Reps", (15, 22), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(self.counter), (100, 60), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, "Press 'q' to escape", (480, 22), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 0), 2, cv2.LINE_AA)

                # Display "Incorrect Form" message if the form is incorrect
                if self.incorrectForm:
                    if elbowAngle < 40:
                        cv2.putText(image, "Incorrect Form: Elbow Too High, Bend Downwards", (10, 180),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    else:
                        cv2.putText(image, "Incorrect Form: Elbow Too Low, Bend Upwards", (10, 180),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (0, 0, 255), 1, cv2.LINE_AA)

                # Draw landmarks on the image
                self.mpDrawing.draw_landmarks(image, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS,
                                              self.mpDrawing.DrawingSpec(color=(245, 117, 66), thickness=2,
                                                                         circle_radius=2),
                                              self.mpDrawing.DrawingSpec(color=(245, 66, 230), thickness=2,
                                                                         circle_radius=2))

                # Display the image
                cv2.imshow("MediaPipe Feed", image)
                cv2.moveWindow("MediaPipe Feed", centerX, centerY)

                # Check if 'q' key is pressed to break the loop
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            # Calculate and display calories burned after the loop ends
            elapsedTime = time.time() - self.startTime
            elapsedTimeHours = elapsedTime / 3600
            cal = self.calorieCalc(self.weight, elapsedTimeHours, self.counter)

            # Display total reps and calories burned on the same image
            cv2.putText(image, f"Calories burned: {cal:.2f}", (7, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 0), 2, cv2.LINE_AA)
            # Display the final results

            cv2.imshow("MediaPipe Feed", image)
            cv2.waitKey(0)  # Wait indefinitely until a key is pressed

            # Release the video capture device and close all OpenCV windows
            cap.release()
            cv2.destroyAllWindows()

            # Go back to the main page after the exercise session
            Gym_GUI.MainPage()


if __name__ == "__main__":
    LeftCurl()  # Replace with appropriate weight value
