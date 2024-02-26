import tkinter as tk
import pyttsx3

def speak_text():
    text = entry.get()
    engine.say(text)
    engine.runAndWait()

# Initialize the Tkinter app
root = tk.Tk()
root.title("Speech to Speech App")

# Create a text entry field
entry = tk.Entry(root, width=50)
entry.pack()

# Create a button to speak the entered text
speak_button = tk.Button(root, text="Speak", command=speak_text)
speak_button.pack()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Run the Tkinter main loop
root.mainloop()