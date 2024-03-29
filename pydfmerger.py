import os
import platform
import subprocess
import tkinter as Tki
from tempfile import mkdtemp
from tkinter.filedialog import askopenfilenames, asksaveasfilename
from tkinter.messagebox import askyesno

from pypdf import PaperSize, PdfMerger, PdfWriter

root = Tki.Tk()
root.title("PyDFGenerator")
width = 547
height = 228
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = "%dx%d+%d+%d" % (
    width,
    height,
    (screenwidth - width) / 2,
    (screenheight - height) / 2,
)
root.geometry(alignstr)
root.resizable(width=False, height=False)

# Listbox
my_listbox = Tki.Listbox(root)
my_listbox.place(x=10, y=10, width=440, height=155)

tempDir = None
filePath = None


def create_empty():
    """creates a temporary file and adds an to it"""
    global tempDir
    if not tempDir:
        tempDir = mkdtemp()
    blankFilePath = tempDir + "/blank.pdf"
    if not os.path.isfile(blankFilePath):
        writer = PdfWriter()
        writer.add_blank_page(PaperSize.A4.width, PaperSize.A4.height)
        with open(blankFilePath, "wb") as output_stream:
            writer.write(output_stream)
        print(blankFilePath)
    return blankFilePath


def insert_empty_page():
    """inserts an empty page with button press"""
    blankFilePath = create_empty()
    my_listbox.insert(Tki.END, blankFilePath)


def merge_pdf():
    """merges pdf and sets file and opens save Dialog"""
    pdfs = list(my_listbox.get(0, Tki.END))
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)

    savePath = save_file()
    merger.write(savePath)
    merger.close()
    answer = askyesno("Open File?", "Merge successful, open merged PDF?")
    if answer:
        invoke_merged_pdf(savePath)


def save_file():
    """opens save dialog"""
    savePath = asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
    )
    return savePath


def invoke_merged_pdf(filePath):
    if platform.system() == "Darwin":
        subprocess.call(("open", filePath))
    elif platform.system() == "Windows":
        os.startfile(filePath)
    else:
        subprocess.call(("xdg-open", filePath))


def open_file():
    """opens file manager and adds the filepath to the listbox"""
    global filePath
    filePath = askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    for item in filePath:
        my_listbox.insert(Tki.END, item)


def move_up():
    """Moves the item at position pos up by one"""
    selected_item = my_listbox.curselection()
    if not selected_item:
        return
    pos = selected_item[0]
    if pos == 0:
        return

    text = my_listbox.get(pos)
    my_listbox.delete(pos)
    my_listbox.insert(pos - 1, text)


def move_down():
    """Moves the item at position pos down by one"""
    selected_item = my_listbox.curselection()
    if not selected_item:
        return
    pos = selected_item[0]
    if pos == my_listbox.size():
        return
    text = my_listbox.get(pos)
    my_listbox.delete(pos)
    my_listbox.insert(pos + 1, text)


MoveUpButton = Tki.Button(root)
MoveUpButton["justify"] = "center"
MoveUpButton["text"] = "↑"
MoveUpButton.place(x=460, y=10, width=70, height=25)
MoveUpButton["command"] = move_up

MoveDownButton = Tki.Button(root)
MoveDownButton["justify"] = "center"
MoveDownButton["text"] = "↓"
MoveDownButton.place(x=460, y=50, width=70, height=25)
MoveDownButton["command"] = move_down

InsertEmptyPageButton = Tki.Button(root)
InsertEmptyPageButton["justify"] = "center"
InsertEmptyPageButton["text"] = "Insert Blank"
InsertEmptyPageButton.place(x=460, y=90, width=70, height=25)
InsertEmptyPageButton["command"] = insert_empty_page

OpenFileButton = Tki.Button(root)
OpenFileButton["justify"] = "center"
OpenFileButton["text"] = "Add File"
OpenFileButton.place(x=460, y=130, width=70, height=25)
OpenFileButton["command"] = open_file

SaveFileButton = Tki.Button(root)
SaveFileButton["fg"] = "#000000"
SaveFileButton["justify"] = "center"
SaveFileButton["text"] = "Merge PDF"
SaveFileButton.place(x=10, y=180, width=522, height=30)
SaveFileButton["command"] = merge_pdf

root.mainloop()
