import tkinter as tk  # Import the tkinter module for GUI creation
from tkinter import ttk, messagebox  # Import ttk for themed widgets and messagebox for dialogs
from PIL import Image, ImageTk  # Import PIL for handling images

# Import custom GUI modules (assumed to exist)
import Left_Elbow_Curl_GUI
import Wide_Push_Up_GUI


class MainPage:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()

        # Set the window title
        self.root.title("Gumnazo")

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

        # Create and display the title text on the canvas
        self.canvas.create_text(250, 50, text="💪Gumnazo🦵", font=("Arial", 20), fill="white")

        # Create and display the exercise selection prompt
        self.canvas.create_text(250, 150, text="Please Select Your Exercise:", font=("Arial", 10), fill="white")

        # Configure the style for the combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="black", background="black", arrowcolor="white",
                        foreground="white", selectbackground="", highlight="")

        # Create a combobox for exercise selection
        self.exerBox = ttk.Combobox(self.root, values=["Wide Arm Push-Up", "Left Arm Curl"])

        # Bind the selection event to a function to update the selected exercise
        self.exerBox.bind("<<ComboboxSelected>>", self.updateExercise)

        # Place the combobox on the window
        self.exerBox.place(x=175, y=170)

        # Create and display the weight input prompt
        self.canvas.create_text(250, 270, text="Please Type in Your Weight in Pounds:", font=("Arial", 10),
                                fill="white")

        # Create an entry widget for weight input with customized colors
        self.weightBox = tk.Entry(self.root, background="Black", fg="white", highlightbackground="White",
                                  insertbackground="White", highlightthickness=2)

        # Configure the style for the combobox when readonly
        style.map('TCombobox',
                  background=[('readonly', 'black')],
                  fieldbackground=[('readonly', 'black')],
                  foreground=[('readonly', 'white')],
                  selectbackground=[('readonly', 'black')],
                  selectforeground=[('readonly', 'white')])

        # Place the entry widget on the window
        self.weightBox.place(x=185, y=290)

        # Create a frame to act as a border for the button
        self.btnBack = tk.Frame(self.root, highlightbackground="White", highlightthickness=2, bd=0)
        self.btnBack.place(x=175, y=382, width=130, height=40)  # Adjust position and size as needed

        # Create a button for proceeding to the next step inside the frame
        self.nextButton = tk.Button(self.btnBack, text="Next", font=("Arial", 10), fg="White", bg="Black",
                                    command=self.decider)
        self.nextButton.pack(fill='both', expand=True)

        # Initialize selected exercise variable
        self.selectedExercise = None

        # Start the main loop of the Tkinter application
        self.root.mainloop()

    def updateExercise(self, event):
        # Update the selected exercise variable with the selected value from the combobox
        self.selectedExercise = self.exerBox.get()

    def decider(self):
        try:
            # Check if an exercise is selected
            if not self.selectedExercise:
                messagebox.showerror("Error", "Please select an exercise.")
                return

            # Convert the weight to float
            weight = float(self.weightBox.get())

            # Decide which exercise's video to play based on the selected exercise
            if self.selectedExercise == "Wide Arm Push-Up":
                self.root.destroy()  # Close the main window
                Wide_Push_Up_GUI.VideoPlayer(weight)  # Call the function to play Wide Push-Up video
            elif self.selectedExercise == "Left Arm Curl":
                self.root.destroy()  # Close the main window
                Left_Elbow_Curl_GUI.VideoPlayer(weight)  # Call the function to play Left Arm Curl video
            else:
                messagebox.showerror("Error", "Invalid exercise selected.")
        except ValueError:
            # Show an error if the weight input is not a valid number
            messagebox.showerror("Error", "Please enter a valid weight.")


# Run the MainPage class only if this script is being executed directly
if __name__ == "__main__":
    MainPage()
