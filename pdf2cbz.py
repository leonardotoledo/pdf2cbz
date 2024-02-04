import os.path
import tkinter as tk
import tkinterdnd2 as tkdnd
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tqdm import tqdm
from converter import convert_pdf_to_cbz


class ProgressDialog(tk.Toplevel):
    def __init__(self, parent, max_value):
        super().__init__(parent)
        self.title("Progress")
        self.geometry("300x100")
        self.progress_var = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate",
                                           variable=self.progress_var, maximum=max_value)
        self.progressbar.pack(pady=20)
        self.update_idletasks()

    def step(self, value=1):
        self.progress_var.set(self.progress_var.get() + value)
        self.update_idletasks()

    def destroy(self):
        super().destroy()


class App:

    def __init__(self, rt):
        self.root = rt
        self.root.title("pdf2cbz")
        self.current_index = None
        self.file_list = []

        # Menu
        # ----
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.help)
        help_menu.add_command(label="About", command=self.about)

        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Add Button
        # -------
        self.add_button = tk.Button(self.root, text="+", command=self.add_file)
        self.add_button.pack(padx=5, anchor=tk.NW, pady=5, side=tk.TOP, fill=tk.BOTH, expand=True)

        # Clear All Button
        # -------
        self.clear_button = tk.Button(self.root, text="Clear All", command=self.clear_list)
        self.clear_button.pack(padx=5, anchor=tk.NE, pady=5, side=tk.TOP, fill=tk.BOTH, expand=True)

        # ListBox
        # -------
        self.listbox = tk.Listbox(self.root, selectmode=tk.EXTENDED)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Convert Button
        # -------
        self.convert_button = tk.Button(rt, text="Convert", command=self.convert)
        self.convert_button.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Enable drag and drop
        # -------
        self.listbox.drop_target_register(tkdnd.DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.drop_event)

    def add_file(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf *.PDF")])
        if filename:
            self.file_list.append(filename)
            self.update_listbox()

    def clear_list(self):
        self.file_list = []
        self.update_listbox()

    def update_listbox(self):
        # Clear listbox
        self.listbox.delete(0, tk.END)

        # Insert filenames
        for filename in self.file_list:
            self.listbox.insert(tk.END, filename)

        # Update listbox
        self.listbox.update_idletasks()
        self.root.update_idletasks()

    def drop_event(self, event):
        # Get the filenames
        filename = ""
        for c in event.data:
            if c == "{":
                filename = ""
            elif c == "}":
                # Check if the file is a PDF
                if filename.endswith(".pdf") or filename.endswith(".PDF"):
                    self.file_list.append(filename)
                else:
                    filename = ""
                    messagebox.showwarning("Warning", "Only PDF files are supported")
            else:
                filename += c

        # Update the listbox
        self.update_listbox()

    def convert(self):
        # Check if there are files to convert
        if not self.file_list:
            messagebox.showwarning("Warning", "No files to convert")
            return

        # Convert files
        progress_dialog = ProgressDialog(self.root, len(self.file_list))
        for filename in tqdm(self.file_list):
            output_path = os.path.splitext(filename)[0] + ".cbz"
            convert_pdf_to_cbz(filename, output_path)
            progress_dialog.step()
        progress_dialog.destroy()
        messagebox.showinfo("Info", "Conversion finished")

        # Clear list
        self.clear_list()

    @staticmethod
    def about():
        messagebox.showinfo("About", "pdf2cbz v1.0\n\nCreated by: leonardotoledo")

    @staticmethod
    def help():
        messagebox.showinfo("Help", "1. Insert or drag PDF files\n2. Click convert")


if __name__ == "__main__":
    root = tkdnd.Tk()
    app = App(root)
    root.mainloop()
