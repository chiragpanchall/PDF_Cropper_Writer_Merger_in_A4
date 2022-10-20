from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk

from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os
from PyPDF2 import PdfMerger,PdfReader,PdfWriter

from welcome2 import getPDF,get4



splash_root = Tk()
splash_root.resizable(False,False)
splash_root.title('PDF cropper')
splash_root.grid()

canvas = Canvas(splash_root, width = 780, height = 460)
canvas.grid(column=0, row=0)
img= (Image.open("welcom.png"))
resized_image= img.resize((780,460), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(resized_image)
canvas.create_image(0, 0, anchor=NW, image=img) 

pb = ttk.Progressbar(
    splash_root, orient='horizontal',
    mode='indeterminate',length=780
)
pb.grid(column=0, row=1)
pb.start()

#Creating the basic window
def main():
	splash_root.destroy()
	root = Tk()
	root.title('PDF cropper')
	root.resizable(False, False)
	root.geometry('780x460')
	open_button = ttk.Button(root,text='Open PDF Files',command=select_files)
	open_button.pack(expand=True)

#Selecting files
def select_files():  
    filenames = fd.askopenfilenames(
        title='Select .PDF files ',
        filetypes=[('PDF file', '*.pdf')])
    merger = PdfMerger()  #Creating object of the PDFMerger and merge all files
    for i in filenames:
            merger.append(i)
    merger.write("mergedpdf.pdf")
    merger.close()
    reader = PdfReader("mergedpdf.pdf")
    writer = PdfWriter()
    for pagenum in range(reader.numPages):    #Cropping the PDF
            page1 = reader.pages[pagenum]
            page1.cropBox.lowerLeft = (170, 170)
            page1.cropBox.lowerRight = (430, 468)
            writer.add_page(page1)
            
    with open("croppedpdf.pdf", "wb") as fp:
            writer.write(fp)

    getPDF("croppedpdf.pdf") #Fit N pages to single pages (MAX = 4)
    showinfo(title='Selected Files',message=filenames)



    #pdf-crop-margins -ap4 15 118 15 367 -p 100 mergedpdf.pdf
    #os.system('pdf-crop-margins -ap4 15 118 15 367 -p 100 mergedpdf.pdf')
    #reader = PdfReader('mergedpdf.pdf')
    #reader.pages[0].mediabox
    #RectangleObject([0, 0, 612, 792])
    #merger.close()
    #os.remove('mergedpdf.pdf')
    #showinfo(title='Selected Files',message=filenames)


splash_root.after(1000,main)
splash_root.attributes('-toolwindow', True)
mainloop()
