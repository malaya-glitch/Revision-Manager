import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # hide main window
file_path = filedialog.askopenfilename(title="Select a file")
print("You selected:", file_path)
