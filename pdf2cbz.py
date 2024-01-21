import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Menu
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import StringVar
from converter import convert_pdf_to_cbz

# Global variables
# ----------------
# GUI
root = tk.Tk()
root.title("pdf2cbz")
root.geometry("620x160")
root.resizable(False, False)

# Variables
input_path = StringVar()
output_path = StringVar()


# Functions
# ---------
def select_input_path():
    input_path.set(filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")]))


def select_output_path():
    output_path.set(filedialog.asksaveasfilename(filetypes=[("CBZ files", "*.cbz")]))


def convert():
    if input_path.get() == "":
        messagebox.showerror("Error", "Please select input path")
        return
    if output_path.get() == "":
        messagebox.showerror("Error", "Please select output path")
        return
    convert_pdf_to_cbz(input_path.get(), output_path.get())
    messagebox.showinfo("Done", "Conversion completed")


def about():
    messagebox.showinfo("About", "pdf2cbz v1.0\n\nCreated by: leonardotoledo")


def help():
    messagebox.showinfo("Help", "1. Select input folder\n2. Select output folder\n3. Click convert")


# Menu
# ----
menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help", command=help)
help_menu.add_command(label="About", command=about)

menu_bar.add_cascade(label="Help", menu=help_menu)

# GUI
# ---
# Input path
input_path_label = Label(root, text="Input path")
input_path_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

input_path_entry = Entry(root, textvariable=input_path, width=50)
input_path_entry.grid(row=0, column=1, padx=10, pady=10, sticky="W")

input_path_button = Button(root, text="Select", command=select_input_path)
input_path_button.grid(row=0, column=2, padx=10, pady=10, sticky="W")

# Output path
output_path_label = Label(root, text="Output path")
output_path_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

output_path_entry = Entry(root, textvariable=output_path, width=50)
output_path_entry.grid(row=1, column=1, padx=10, pady=10, sticky="W")

output_path_button = Button(root, text="Select", command=select_output_path)
output_path_button.grid(row=1, column=2, padx=10, pady=10, sticky="W")

# Convert button
convert_button = Button(root, text="Convert", command=convert)
convert_button.grid(row=2, column=1, padx=10, pady=10, sticky="W")

# Main loop
# ---------
root.mainloop()
